from django.db import models
from django.utils import timezone

from main.models import CustomUser


def image_profile_path(instance, filename):
    restaurant_name = instance.name
    restaurant_address = instance.address

    return f"{restaurant_name}/{restaurant_address}/profile_image/{filename}"


def image_restaurant_path(instance, filename):
    restaurant_name = instance.name
    restaurant_address = instance.address

    return f"{restaurant_name}/{restaurant_address}/restaurant_images/{filename}"


class Kitchen(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class VisitPurpose(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Feature(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}"


class Restaurant(models.Model):
    name = models.CharField('Название ресторана', max_length=255)
    address = models.CharField('Адрес ресторана', max_length=255)
    contact_number = models.CharField('Контактный номер', max_length=11, blank=True, null=True, unique=True)
    min_average_check = models.PositiveIntegerField()
    max_average_check = models.PositiveIntegerField()

    description = models.TextField("Описание")

    kitchens = models.ManyToManyField(Kitchen)
    visit_purposes = models.ManyToManyField(VisitPurpose)
    features = models.ManyToManyField(Feature)

    restaurant_image = models.ImageField(upload_to=image_profile_path, max_length=255, null=True, blank=True,
                                         verbose_name="Фотография профиля ресторана")
    photo_1 = models.ImageField(upload_to=image_restaurant_path, max_length=255, null=True, blank=True,
                                verbose_name="Первая фотография ресторана")
    photo_2 = models.ImageField(upload_to=image_restaurant_path, max_length=255, null=True, blank=True,
                                verbose_name="Вторая фотография ресторана")
    photo_3 = models.ImageField(upload_to=image_restaurant_path, max_length=255, null=True, blank=True,
                                verbose_name="Третья фотография ресторана")

    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='restaurants')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='restaurants')

    status = models.BooleanField(default=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'

    def save(self, *args, **kwargs):
        # Нормализуем номер перед сохранением в базу данных
        if self.contact_number:
            normalized_number = self.normalize_phone_number(self.contact_number)
            if normalized_number:
                self.contact_number = normalized_number
            else:
                raise ValueError("Неправильный формат номера телефона")

        super().save(*args, **kwargs)

    def normalize_phone_number(self, number):
        # Убираем все символы, кроме цифр
        digits = ''.join(filter(str.isdigit, number))

        # Если номер имеет 11 символов, оставляем его без изменений
        if len(digits) == 11:
            return digits
        return number

    def get_absolute_url(self):
        return f'/restaurants/{self.name}/{self.id}/'

    def __str__(self):
        return f'{self.name}, {self.address}'


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    number = models.IntegerField('Номер стола')
    capacity = models.IntegerField('Вместимость')
    photo = models.ImageField(upload_to='photos/tables/', max_length=255, null=True, blank=True,
                              verbose_name='Фотография стола')
    x_in_map = models.PositiveIntegerField('Координаты X')
    y_in_map = models.PositiveIntegerField('Координаты Y')

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'

    def __str__(self):
        return f"Стол №{self.number} (Вместимость: {self.capacity})"


class Reservation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    name = models.CharField('ФИО', max_length=255)
    count_guess = models.PositiveIntegerField('Количество человек')
    phone = models.CharField('Номер телефона', max_length=15)
    additional_info = models.TextField('Дополнительная информация', max_length=300, blank=True, null=True)

    is_accepted = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)


class WorkTime(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name='worktime')
    monday_opening_time = models.TimeField()
    monday_closing_time = models.TimeField()
    tuesday_opening_time = models.TimeField()
    tuesday_closing_time = models.TimeField()
    wednesday_opening_time = models.TimeField()
    wednesday_closing_time = models.TimeField()
    thursday_opening_time = models.TimeField()
    thursday_closing_time = models.TimeField()
    friday_opening_time = models.TimeField()
    friday_closing_time = models.TimeField()
    saturday_opening_time = models.TimeField()
    saturday_closing_time = models.TimeField()
    sunday_opening_time = models.TimeField()
    sunday_closing_time = models.TimeField()

    class Meta:
        verbose_name = 'График работы'
        verbose_name_plural = 'Графики работ'

    def __str__(self):
        return f"Рабочий график ресторана {self.restaurant.name}, {self.restaurant.address}"


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    reviewer_name = models.CharField('Имя и фамилия',max_length=255)
    comment = models.TextField('Комментарий', blank=True, null=True)
    rating = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.restaurant.name} - {self.reviewer_name}'
