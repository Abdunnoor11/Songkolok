# Generated by Django 3.0.7 on 2021-02-14 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0022_poster'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poster',
            old_name='poster',
            new_name='img',
        ),
    ]
