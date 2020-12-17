from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe,
                     ShoppingList, Tag, UserFollow)


class FavoriteAdmin(admin.ModelAdmin):
    pass


class IngredientAdmin(admin.ModelAdmin):
    pass


class RecipeAdmin(admin.ModelAdmin):
    pass


class ShoppingListAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


class UserFollowAdmin(admin.ModelAdmin):
    pass


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(UserFollow, UserFollowAdmin)
