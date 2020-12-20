from django.shortcuts import get_object_or_404


from .models import IngredientQuantity, Ingredient


def extract_ingredients_table(post_data):
    search_tuple = ('nameIngredient_', 'valueIngredient_', 'unitsIngredient_')
    delimetr = 'Ingredient_'

    ingredients_table = {}
    for key, value in post_data.items():
        if key.startswith(search_tuple):
            attr, index = key.split(sep=delimetr)
            ingredients_table[index] = ingredients_table.get(index, {})
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
