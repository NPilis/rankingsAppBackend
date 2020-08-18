# Generated by Django 3.1 on 2020-08-10 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ranking', '0003_auto_20200808_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rankingposition',
            name='ranking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rankig_positions', to='ranking.ranking'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('ranking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ranking.ranking')),
                ('reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='ranking.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
