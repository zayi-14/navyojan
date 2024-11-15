# Generated by Django 4.2.9 on 2024-01-16 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scholarship_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('last_date', models.DateTimeField(auto_now_add=True)),
                ('offered_by', models.CharField(max_length=250)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('state', models.CharField(max_length=250)),
            ],
        ),
    ]
