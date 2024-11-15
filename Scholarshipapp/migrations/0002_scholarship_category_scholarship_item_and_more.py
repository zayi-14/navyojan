# Generated by Django 4.2.9 on 2024-01-17 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Scholarshipapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scholarship_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('description', models.CharField(max_length=350)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='Scholarship_category')),
            ],
            options={
                'verbose_name': 'scholarship_category',
                'verbose_name_plural': 'scholarship_categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Scholarship_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('last_date', models.DateTimeField(auto_now_add=True)),
                ('offered_by', models.CharField(max_length=250)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('state', models.CharField(max_length=250)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Scholarshipapp.scholarship_category')),
            ],
            options={
                'verbose_name': 'scholarship_item',
                'verbose_name_plural': 'scholarship_items',
                'ordering': ('name',),
            },
        ),
        migrations.DeleteModel(
            name='Scholarship_details',
        ),
    ]
