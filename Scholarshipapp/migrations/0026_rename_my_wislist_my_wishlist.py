# Generated by Django 5.0.2 on 2024-06-06 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Scholarshipapp', '0025_rename_scholarship_my_wislist_scholarships'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='my_wislist',
            new_name='my_wishlist',
        ),
    ]
