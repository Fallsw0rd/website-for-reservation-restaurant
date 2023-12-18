from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group


class CustomUser(AbstractUser):
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    name = models.CharField(max_length=100, verbose_name="Имя")
    middlename = models.CharField(max_length=100, verbose_name="Отчество")
    email = models.EmailField(verbose_name='Почтовый адрес', unique=True)
    fullname = models.CharField(max_length=100, verbose_name="ФИО")
    phone_number = models.CharField(max_length=100, verbose_name="Номер телефона", unique=True)
    avatar = models.ImageField(upload_to='Users', max_length=255, null=True, blank=True)

    # Поле groups, определенное в AbstractUser
    groups = models.ManyToManyField(Group, blank=True)

    # Поле user_permissions, определенное в AbstractUser
    user_permissions = models.ManyToManyField(Permission, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

