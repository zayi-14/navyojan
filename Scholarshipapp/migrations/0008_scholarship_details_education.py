# Generated by Django 5.0.2 on 2024-05-30 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scholarshipapp', '0007_scholarship_details_scholarship_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship_details',
            name='Education',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Scholarshipapp.education'),
        ),
    ]
