# Generated by Django 3.1 on 2020-08-20 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0004_auto_20200811_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rankingposition',
            name='ranking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ranking_positions', to='ranking.ranking'),
        ),
    ]
