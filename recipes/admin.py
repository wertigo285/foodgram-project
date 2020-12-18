from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe,
                     ShoppingList, Tag, Subscription, IngredientQuantity)


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


class SubscriptionAdmin(admin.ModelAdmin):
    pass

class IngredientQuantityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(IngredientQuantity, IngredientQuantityAdmin)
