from django.db import models


class Bill(models.Model):
    client_name = models.CharField(max_length=200)
    client_org = models.CharField(max_length=200)
    number = models.PositiveIntegerField()
    sum = models.FloatField()  #
    date = models.DateTimeField()  # To save the timezone information
    service = models.TextField()
