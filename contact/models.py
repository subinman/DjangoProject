from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()  # Removed unique=True
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name
