# Generated by Django 5.0.2 on 2024-07-01 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scholarshipapp', '0028_remove_scholarship_details_plan_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
