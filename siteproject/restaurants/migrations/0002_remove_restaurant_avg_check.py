# Generated by Django 4.2.7 on 2023-11-26 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='avg_check',
        ),
    ]