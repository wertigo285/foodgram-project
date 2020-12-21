import json
import os
import sys

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'foodgram.settings'
django.setup()

from recipes.models import Tag, Ingredient

if __name__ == '__main__':
    classes = globals().keys()
    path = f'{sys.path[0]}\\front\\static\\ingredients.json'
    with open(path, 'r') as file:
        data = json.loads(''.join(file.readlines()))
        for ingredient in data:
            inst = Ingredient(**ingredient)
            try:
                inst.save()
            except:
                pass

    Tag(title='Завтрак', color='orange').save()
    Tag(title='Обед', color='green').save()
    Tag(title='Ужин', color='purple').save()
    print('Данные загружены')
