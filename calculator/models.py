from django.db import models


class Product(models.Model):
    name = models.CharField(max_length = 30)
    calories = models.IntegerField()
    bilky = models.IntegerField()
    zhury = models.IntegerField()
    vuglevody = models.IntegerField()

    def __str__(self):
        return self.name
