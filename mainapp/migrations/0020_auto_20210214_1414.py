# Generated by Django 3.0.7 on 2021-02-14 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0019_auto_20210214_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_img',
            field=models.ImageField(blank=True, upload_to='pics'),
        ),
    ]
