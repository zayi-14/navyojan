# Generated by Django 5.0.2 on 2024-06-02 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scholarshipapp', '0014_rename_userplan_userplanscholarship'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_plan',
            name='plan_image',
            field=models.FileField(null=True, upload_to='plan_image'),
        ),
    ]
