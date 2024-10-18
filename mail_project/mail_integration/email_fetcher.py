import imaplib
import email
from email.header import decode_header
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
from .models import EmailMessage, EmailAccount
from email.utils import parsedate_to_datetime

def fetch_emails(email_account):
    # Сохраняем или обновляем учетную запись перед началом получения писем
    account, created = EmailAccount.objects.get_or_create(
        email=email_account.email,
        defaults={'password': email_account.password}
    )

    
    # Если учетная запись существует, но пароль изменился, обновляем его
    if not created and account.password != email_account.password:
        account.password = email_account.password
        account.save()

    # Логика получения сообщений
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(account.email, account.password)
    mail.select('inbox')

    # Получение списка идентификаторов сообщений
    result, data = mail.search(None, 'ALL')
    email_ids = data[0].split()
    total_emails = len(email_ids)

    channel_layer = get_channel_layer()
    progress = 0

    for email_id in email_ids:
        result, msg_data = mail.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        # Декодирование заголовков
        subject, encoding = decode_header(msg['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else 'utf-8')

        date_sent = msg['Date']
        # Преобразуем строку даты в объект datetime
        date_sent = parsedate_to_datetime(date_sent)

        def get_email_body(msg):
            # Если сообщение состоит из нескольких частей, обрабатываем каждую из них
            if msg.is_multipart():
                # Ищем текстовую часть сообщения
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        return part.get_payload(decode=True).decode(part.get_content_charset())
            else:
                # Если сообщение не многочастное, возвращаем его содержимое
                return msg.get_payload(decode=True).decode(msg.get_content_charset())

            return "Текст сообщения недоступен"  # Возвращаем сообщение, если ничего не нашли

        # Получение тела сообщения
        body = get_email_body(msg)

        # Сохранение сообщения в БД и привязка его к учетной записи
        EmailMessage.objects.create(
            email_account=account,  # Привязываем сообщение к учетной записи
            subject=subject,
            date_sent=date_sent,  # Преобразованная дата отправки
            date_received=datetime.now(),  # Дата получения (текущая)
            body=body,
            attachments=[],  # Можно добавить обработку вложений
        )


        # Обновление прогресса
        progress += 1
        async_to_sync(channel_layer.group_send)(
            "progress_group",
            {
                "type": "progress_update",
                "progress": int((progress / total_emails) * 100),
            },
        )

    mail.logout()
