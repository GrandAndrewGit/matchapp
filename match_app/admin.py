from django.contrib import admin
from .models import DataSet, UserFromData


class DataSetAdmin(admin.ModelAdmin):
    model = DataSet
    list_display = ('id', 'date_created')

admin.site.register(DataSet, DataSetAdmin)


class UserFromDataAdmin(admin.ModelAdmin):
    model = UserFromData
    list_display = ('id', 'username')

admin.site.register(UserFromData, UserFromDataAdmin)