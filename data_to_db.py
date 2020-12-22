import json
import os
from collections import defaultdict


import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'foodgram.settings'
django.setup()

from recipes.models import Tag, Ingredient

if __name__ == '__main__':
    classes = globals().keys()

    path = os.path.dirname(__file__)
    path = os.path.join(path, 'front', 'static', 'ingredients.json')
    with open(path, 'rb') as file:
        data = json.load(file)
        # Словарь для избежания дублей
        ingredients = defaultdict()
        for ingredient in data:
            key = tuple([value for value in ingredient.values()])
            ingredients[key] = Ingredient(**ingredient)

    Ingredient.objects.bulk_create(ingredients.values())

    Tag(title='Завтрак', color='orange').save()
    Tag(title='Обед', color='green').save()
    Tag(title='Ужин', color='purple').save()

    print('Данные загружены')
