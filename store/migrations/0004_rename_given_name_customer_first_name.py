# Generated by Django 4.0.5 on 2022-07-12 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rename_first_name_customer_given_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='given_name',
            new_name='first_name',
        ),
    ]
