# Generated by Django 4.2.7 on 2023-12-01 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_restaurant_max_average_check_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер стола')),
                ('capacity', models.IntegerField(verbose_name='Вместимость')),
                ('photo', models.ImageField(blank=True, max_length=255, null=True, upload_to='photos/tables/', verbose_name='Фотография стола')),
                ('is_available', models.BooleanField(default=True)),
                ('x_in_map', models.PositiveIntegerField(verbose_name='Координаты X')),
                ('y_in_map', models.PositiveIntegerField(verbose_name='Координаты Y')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant')),
            ],
            options={
                'verbose_name': 'Стол',
                'verbose_name_plural': 'Столы',
            },
        ),
    ]