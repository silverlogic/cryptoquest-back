from django.db import models


class Coin(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name
