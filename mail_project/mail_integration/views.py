from django.shortcuts import render
from .models import EmailMessage, EmailAccount
from .email_fetcher import fetch_emails

def messages_list(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Сохраняем учетную запись в базе данных, если она еще не существует
        email_account, created = EmailAccount.objects.get_or_create(
            email=email,
            defaults={'password': password}
        )

        if not created:  # Если учетная запись уже существует, обновляем пароль
            email_account.password = password
            email_account.save()

        # Вызов функции для получения имейлов с учетной записью из базы
        fetch_emails(email_account)

    messages = EmailMessage.objects.all()  # Получаем все сообщения из базы данных
    return render(request, 'messages_list.html', {'messages': messages})
