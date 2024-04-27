from django.contrib import admin
from .models import Restaurant, WorkTime, Table, TableAdditionRequest, MapAdditionRequest

admin.site.register(Restaurant)
admin.site.register(WorkTime)
admin.site.register(Table)
admin.site.register(MapAdditionRequest)
admin.site.register(TableAdditionRequest)
