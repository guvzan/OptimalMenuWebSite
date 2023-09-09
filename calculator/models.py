from django.db import models


class Product(models.Model):
    name = models.CharField(max_length = 200)
    calories = models.FloatField()
    bilky = models.FloatField()
    zhury = models.FloatField()
    vuglevody = models.FloatField()

    def __str__(self):
        return self.name
