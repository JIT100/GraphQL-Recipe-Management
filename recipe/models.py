from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    instructions = models.TextField(blank=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes', blank=True)

    def __str__(self):
        return self.name
