# Generated by Django 3.0.7 on 2021-02-22 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0026_auto_20210222_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=70, null=True, unique=True),
        ),
    ]
