from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


from unidecode import unidecode


User = get_user_model()


class Recipe(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recieps/')
    description = models.TextField()
    ingredients = models.ManyToManyField(
        'Ingredient', through='IngredientQuantity')
    tags = models.ManyToManyField('Tag', related_name='recipes', blank=True)
    duration = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'dimension'], name='unique_ingredient')
        ]

    def __str__(self):
        return self.title


class IngredientQuantity(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return f'{self.recipe.title} ({self.ingredient.title} - {self.quantity} {self.ingredient.dimension})'


class Tag(models.Model):
    title = models.CharField(max_length=20)
    color = models.CharField(max_length=20, null=False, default='', blank=True)
    slug = models.SlugField(max_length=20)

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followings')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscription')
        ]

    def __str__(self):
        return f'Подписка {self.user.username} на {self.author.username}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='users_favorite')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite')
        ]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite')
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном {self.user.username}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_lists')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_lists')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_position')
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном {self.user.username}'
