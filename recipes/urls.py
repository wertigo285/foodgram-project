from django.urls import path

from .views import index, subscriptions, favorites, recipe_view, author_view

urlpatterns = [
    path('', index, name='index'),
    path('favorites/', favorites, name='favorites'),
    path('recipes/<int:recipe_id>/', recipe_view, name='recipe'),
    path('authors/<int:author_id>/', author_view, name='author'),
    path('subscriptions/', subscriptions, name='subscriptions')
]