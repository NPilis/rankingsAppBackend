# Generated by Django 3.1 on 2020-11-13 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0013_auto_20201113_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ranking',
            name='image',
            field=models.ImageField(blank=True, upload_to='ranking/'),
        ),
        migrations.AlterField(
            model_name='rankingposition',
            name='image',
            field=models.ImageField(blank=True, upload_to='position/'),
        ),
    ]
