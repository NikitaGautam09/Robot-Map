# app/models.py

from django.db import models

class Mission(models.Model):
    mission_number = models.IntegerField()
    status = models.CharField(max_length=10, default='Pending')
