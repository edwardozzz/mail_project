from django.db import models

class EmailAccount(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

class EmailMessage(models.Model):
    email_account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE, related_name='messages')
    subject = models.CharField(max_length=255)
    date_sent = models.DateTimeField()
    date_received = models.DateTimeField()
    body = models.TextField()
    attachments = models.JSONField()