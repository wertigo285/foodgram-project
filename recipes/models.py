from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from unidecode import unidecode

User = get_user_model()

class Recipe(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recieps/', blank=True, null=True)
    description = models.TextField()
    ingredients = models.ManyToManyField(
        'Ingredient', through='IngredientQuantity')
    tags = models.ManyToManyField('Tag', related_name='recipes')
    duration = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['-pub_date']

    def get_duration(self):
        result = ''
        hours = self.duration // 60
        if hours:
            result += f'{hours} ч. '
        minutes = self.duration % 60
        if minutes:
            result += f'{minutes} мин.'
        return result.strip()


class Ingredient(models.Model):
    title = models.CharField(max_length=100)
    dimension = models.CharField(max_length=20)


class IngredientQuantity(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.FloatField()


class Tag(models.Model):

    title = models.CharField(max_length=20)
    color = models.CharField(max_length=20, null=False, default='', blank=True)
    slug = models.SlugField(max_length=20)

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        super(Tag, self).save(*args, **kwargs)


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followings')


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='users_favorite')


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_lists')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_lists')
    
