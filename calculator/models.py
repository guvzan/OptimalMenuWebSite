from django.db import models


class Product(models.Model):
    name = models.CharField(max_length = 200)
    calories = models.FloatField()
    bilky = models.FloatField()
    zhury = models.FloatField()
    vuglevody = models.FloatField()

    def __str__(self):
        return self.name


class ApprovedMenu(models.Model):
    calories = models.FloatField()
    bzu = models.CharField(max_length=200)
    menu = models.TextField()

    def get_calories(self):
        return int(float(self.calories))

    def get_bzu(self):
        list_ = self.bzu[1:-1].split(',')
        for i in range(len(list_)):
            list_[i] = int(float(list_[i]))
        return list_

    def get_menu(self):
        return self.menu[1:-1].split(',')
