from django.contrib import admin
from .models import Restaurant, WorkTime, Table

admin.site.register(Restaurant)
admin.site.register(WorkTime)
admin.site.register(Table)