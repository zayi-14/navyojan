# Generated by Django 4.2.9 on 2024-02-23 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration_app', '0006_delete_payment_webhook'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_webhook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_amount', models.IntegerField()),
                ('checkout_session_id', models.CharField(max_length=250)),
                ('payment_intent_id', models.CharField(max_length=250, null=True)),
                ('payment_date', models.DateTimeField()),
                ('payment_status', models.CharField(max_length=250, null=True)),
                ('expiry_date', models.CharField(max_length=250, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration_app.customuser')),
            ],
        ),
    ]
