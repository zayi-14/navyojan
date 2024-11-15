# Generated by Django 5.0.2 on 2024-05-29 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scholarshipapp', '0005_register_re_password_register_states'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='Age',
        ),
        migrations.AddField(
            model_name='register',
            name='dob',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='register',
            name='u_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='scholarship_details',
            name='Scholar_Description',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
    ]