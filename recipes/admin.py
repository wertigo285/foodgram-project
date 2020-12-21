from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe,
                     ShoppingList, Tag, Subscription, IngredientQuantity)


class FavoriteAdmin(admin.ModelAdmin):
    pass


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension',)
    list_filter = ('title',)


class RecipeAdmin(admin.ModelAdmin):
    ist_display = ('title', 'author', 'show_favorites')
    list_filter = ('author', 'title', 'tags',)
    list_select_related = True

    def show_favorites(self, obj):
        result = Favorite.objects.filter(recipe=obj).count()
        return result

    show_favorites.short_description = "Favorite"


class ShoppingListAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'color')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class IngredientQuantityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(IngredientQuantity, IngredientQuantityAdmin)
