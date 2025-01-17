# Generated by Django 5.1.2 on 2024-10-18 03:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_integration', '0003_remove_emailmessage_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailmessage',
            name='email_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mail_integration.emailaccount'),
        ),
        migrations.AlterField(
            model_name='emailmessage',
            name='attachments',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
