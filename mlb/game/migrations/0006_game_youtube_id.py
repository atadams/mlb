# Generated by Django 2.2.8 on 2019-12-14 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20191214_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='youtube_id',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]