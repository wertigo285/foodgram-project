import json


from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.transaction import atomic
from django.db.models import Count, OuterRef, Prefetch, Subquery
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.views.decorators.http import require_http_methods


from .forms import RecipeForm
from .models import (Favorite, Ingredient, IngredientQuantity,
                     Recipe, Subscription, ShoppingList, Tag, User)
from .utilities import set_ingredients, get_recipes_qs


def index(request):
    tags = Tag.objects.all()

    user = request.user

    recipes = get_recipes_qs(user)

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'page': page, 'paginator': paginator,
               'tags': tags, 'title': 'Рецепты'}
    return render(request, 'index.html', context=context)


def author_view(request, author_id):
    tags = Tag.objects.all()

    user = request.user

    author = get_object_or_404(User, pk=author_id)

    recipes = get_recipes_qs(user).filter(author=author)

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'page': page, 'paginator': paginator,
               'tags': tags, 'title': author.first_name}
    return render(request, 'index.html', context=context)


@ login_required
def favorites(request):
    tags = Tag.objects.all()

    user = request.user

    recipes = get_recipes_qs(user).filter(users_favorite__user=user)

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'page': page, 'paginator': paginator,
               'tags': tags, 'title': 'Избранное'}
    return render(request, 'index.html', context=context)


@ login_required
def subscriptions(request):
    user = request.user

    # Лимитирование запроса генерируемого prefetch_related
    # https://code.djangoproject.com/ticket/26780#comment:6
    feed_length = 3
    authors = User.objects.filter(
        followings__user=user
    ).annotate(
        recipe_count=Count(
            'recipes'
        )
    ).prefetch_related(
        Prefetch(
            'recipes', queryset=Recipe.objects.filter(
                id__in=Subquery(
                    Recipe.objects.filter(
                        author_id=OuterRef(
                            'author_id'
                        )).values_list(
                        'id',
                        flat=True
                    )[:feed_length]
                ))))

    paginator = Paginator(authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'page': page, 'paginator': paginator,
               'feed_length': feed_length, 'title': 'Мои подписки'}
    return render(request, 'follow.html', context=context)


def recipe_view(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(get_recipes_qs(user), pk=recipe_id)

    ingredients = zip(recipe.ingredients.all(),
                      recipe.ingredientquantity_set.all())

    return render(request, 'single_page.html', context={'recipe': recipe, 'ingredients': ingredients})


@ login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user != recipe.author:
        return redirect(to='recipe', recipe_view=recipe_id)

    form = RecipeForm(request.POST or None,
                      files=request.FILES or None, instance=recipe)

    if request.method == 'POST':
        if form.is_valid():
            recipe = form.save(commit=False)
            with atomic():
                recipe.save()
                set_ingredients(request.POST, recipe)
                form.save_m2m()
            return redirect(to='recipe', recipe_id=recipe.pk)

    ingredients = IngredientQuantity.objects.filter(
        recipe=recipe
    ).select_related(
        'ingredient'
    ).values(
        'pk', 'quantity', 'ingredient__title', 'ingredient__dimension'
    ).order_by(
        'pk'
    )

    return render(request, 'recipe_form.html', context={'form': form, 'ingredients': list(ingredients)})


@ login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user != recipe.author:
        return redirect(to='recipe', recipe_view=recipe_id)

    recipe.delete()

    return redirect(to='index')


@ login_required
def recipe_new(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            with atomic():
                recipe.save()
                set_ingredients(request.POST, recipe)
                form.save_m2m()
            return redirect(to='recipe', recipe_id=recipe.pk)

    return render(request, 'recipe_form.html', context={'form': form})


@ login_required
def shopping_list(request):
    user = request.user
    shopping_list = ShoppingList.objects.filter(user=user)
    return render(request, 'shopping_list.html', context={'shopping_list': shopping_list})


@ login_required
@ require_http_methods(['GET'])
def ingredients_js(request):
    query = request.GET['query']
    data = Ingredient.objects.filter(
        title__icontains=query).values('title', 'dimension')

    return JsonResponse(list(data), safe=False)


@ login_required
@ require_http_methods(['POST', 'DELETE'])
def favorites_js(request, recipe_id=None):
    user = request.user
    if request.method == 'POST':
        data = json.loads(request.body)
        recipe = get_object_or_404(Recipe, pk=data['id'])
        Favorite.objects.create(user=user, recipe=recipe)
    else:
        fav = get_object_or_404(Favorite, user=user, recipe__id=recipe_id)
        fav.delete()

    return JsonResponse(data={})


@ login_required
@ require_http_methods(['POST', 'DELETE'])
def subscriptions_js(request, author_id=None):
    user = request.user
    if request.method == 'POST':
        data = json.loads(request.body)
        author = get_object_or_404(User, pk=data['id'])
        Subscription.objects.create(user=user, author=author)
    else:
        sub = get_object_or_404(Subscription, user=user, author__id=author_id)
        sub.delete()

    return JsonResponse(data={})


@ login_required
@ require_http_methods(['POST', 'DELETE'])
def purchases_js(request, recipe_id=None):
    user = request.user
    if request.method == 'POST':
        data = json.loads(request.body)
        recipe = get_object_or_404(Recipe, pk=data['id'])
        ShoppingList.objects.create(user=user, recipe=recipe)
    else:
        sub = get_object_or_404(ShoppingList, user=user, recipe__id=recipe_id)
        sub.delete()

    return JsonResponse(data={})
