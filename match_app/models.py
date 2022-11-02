from django.db import models
from django.utils import timezone


class DataSet(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    csv_file = models.FileField(upload_to='datafiles/')
    xml_file = models.FileField(upload_to='datafiles/')
    processed_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class UserFromData(models.Model):
    username = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=50, blank=False)
    avatar = models.CharField(max_length=160, blank=False)
    is_unique = models.BooleanField(default=True)

    def __str__(self):
        return self.username
