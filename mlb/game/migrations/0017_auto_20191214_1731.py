# Generated by Django 2.2.8 on 2019-12-14 23:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_auto_20191214_1727'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inning',
            options={'ordering': ['inning']},
        ),
    ]
