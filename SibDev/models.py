from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Url(models.Model):
    name = models.CharField(max_length = 255)
    minutes = models.IntegerField(validators = [MinValueValidator(0)])
    seconds = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(59)])
    site_info = models.TextField(blank = 'true')

    def __str__(self):
        return self.name
