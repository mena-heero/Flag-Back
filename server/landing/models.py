from django.db import models

class Lead(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.email


