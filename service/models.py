from django.db import models

class Service(models.Model):
    service_icon = models.CharField(max_length=50)
    service_title = models.CharField(max_length=50)
    service_description = models.TextField()

    def __str__(self):
        return self.service_title

class UsersForm(models.Model):  # Corrected class name
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name



