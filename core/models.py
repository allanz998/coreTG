from django.db import models
from django.contrib import admin


class File(models.Model):
    name = models.CharField(max_length=255)
    path = models.FileField(upload_to='vpnfiles/', null=True, blank=True)
    description = models.TextField(max_length=255, default="") 
    sent = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name