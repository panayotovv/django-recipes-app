from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=CASCADE)
    quantity = models.FloatField(null=True, blank=True, default='')
    unit = models.CharField(max_length=10, null=True, blank=True, default='')

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.ingredient.name}"


class Instructions(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        default='default.jpg'
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    prep_time = models.PositiveIntegerField()
    cook_time = models.PositiveIntegerField()
    description = models.TextField()

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes'
    )
    instructions = models.OneToOneField(to=Instructions, on_delete=CASCADE)
    favorited_by = models.ManyToManyField(User, related_name='favorite_recipes', blank=True)
    author = models.ForeignKey(to=User, related_name='recipes', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title



