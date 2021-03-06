from collections import defaultdict


from django.db.models import Prefetch
from django.shortcuts import get_object_or_404


from .models import (Favorite, IngredientQuantity,
                     Ingredient, Recipe, ShoppingList,
                     Subscription, Tag)


def get_tags(req_get_data):

    tags = Tag.objects.all()

    tags_values = req_get_data.getlist('tags')

    if not tags_values:
        tags_values = [tag.slug for tag in tags]

    return (tags, tags_values)


def get_recipes_qs(user):
    return Recipe.objects.select_related(
        'author'
    ).prefetch_related(
        'tags',
        Prefetch(
            'users_favorite', queryset=Favorite.objects.filter(
                user=user
            )),
        Prefetch(
            'author__followers', queryset=Subscription.objects.filter(
                user=user
            )),
        Prefetch('shopping_lists', queryset=ShoppingList.objects.filter(
            user=user)))


def extract_ingredients_table(post_data):
    search_tuple = ('nameIngredient_', 'valueIngredient_', 'unitsIngredient_')
    delimetr = 'Ingredient_'
    ingredients_table = defaultdict(dict)
    for key, value in post_data.items():
        if key.startswith(search_tuple):
            attr, index = key.split(sep=delimetr)
            ingredients_table[index][attr] = value

    return ingredients_table


def set_ingredients(post_data, recipe):
    ingredients_table = extract_ingredients_table(post_data)

    recipe.ingredients.clear()

    new_ingredients = []
    for string in ingredients_table.values():
        title, dimension, quantity = string['name'], string['units'], float(
            string['value'].replace(',', '.'))
        ingredient = get_object_or_404(
            Ingredient, title=title, dimension=dimension)
        new_ingredients.append(IngredientQuantity(
            ingredient=ingredient, recipe=recipe, quantity=quantity))

    IngredientQuantity.objects.bulk_create(new_ingredients)
