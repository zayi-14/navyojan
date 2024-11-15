# Generated by Django 4.2.9 on 2024-02-23 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration_app', '0004_remove_payment_webhook_user_id_payment_webhook_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment_webhook',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
