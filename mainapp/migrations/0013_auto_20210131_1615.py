# Generated by Django 3.0.7 on 2021-01-31 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_auto_20210131_1604'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderHistory',
            new_name='OrderItem',
        ),
    ]
