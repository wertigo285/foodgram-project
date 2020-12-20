from django.urls import path


from .views import (author_view, favorites, favorites_js, index, ingredients_js,
                    recipe_delete, recipe_edit, recipe_new, recipe_view, subscriptions, 
                    subscriptions_js)


urlpatterns = [
    path('', index, name='index'),
    path('new/', recipe_new, name='recipe_new'),
    path('favorites/', favorites, name='favorites'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('authors/<int:author_id>/', author_view, name='author'),
    path('recipes/<int:recipe_id>/', recipe_view, name='recipe'),
    path('recipes/<int:recipe_id>/edit/', recipe_edit, name='recipe_edit'),
    path('recipes/<int:recipe_id>/edit/delete/', recipe_delete, name='recipe_delete'),
    path('ingredients', ingredients_js, name='ingredients'),
    path('favorites', favorites_js),
    path('favorites/<int:recipe_id>/', favorites_js),
    path('subscriptions', subscriptions_js),
    path('subscriptions/<int:author_id>/', subscriptions_js),
]
