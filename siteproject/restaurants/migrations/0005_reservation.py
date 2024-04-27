# Generated by Django 4.2.7 on 2023-12-01 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0004_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('name', models.CharField(max_length=255, verbose_name='ФИО')),
                ('count_guess', models.PositiveIntegerField(verbose_name='Количество человек')),
                ('phone', models.CharField(max_length=15, verbose_name='Номер телефона')),
                ('additional_info', models.TextField(blank=True, max_length=300, null=True, verbose_name='Дополнительная информация')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.table')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]