# Generated by Django 3.1a1 on 2020-06-01 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_highscore'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='highscore',
            options={'ordering': ('-score',)},
        ),
    ]
