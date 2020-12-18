from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator


from .models import (Recipe, Tag, User, Subscription)


def index(request):

    tags = Tag.objects.all()

    recipes = Recipe.objects.select_related(
        'author').prefetch_related('tags').all()
    paginator = Paginator(recipes, 6)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'page': page, 'paginator': paginator,
               'tags': tags, 'title': 'Рецепты'}
    return render(request, 'index.html', context=context)

def author_view(request,author_id):

    author = get_object_or_404(User,pk=author_id)

    tags = Tag.objects.all()

    recipes = author.recipes.select_related(
        'author').prefetch_related('tags').all()
    paginator = Paginator(recipes, 6)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'page': page, 'paginator': paginator,
               'tags': tags, 'title': author.first_name}
    return render(request, 'index.html', context=context)

@login_required
def favorites(request):

    user = request.user

    tags = Tag.objects.all()

    recipes = Recipe.objects.select_related('author').prefetch_related(
        'tags').filter(users_favorite__user=user)
    paginator = Paginator(recipes, 6)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'page': page, 'paginator': paginator,
               'tags': tags, 'title': 'Избранное'}
    return render(request, 'index.html', context=context)

@login_required
def subscriptions(request):

    user = request.user
    authors = User.objects.prefetch_related('recipes').filter(followings__user=user)

    
    paginator = Paginator(authors, 6)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'page': page, 'paginator': paginator,
                'title': 'Мои подписки'}
    return render(request, 'follow.html', context=context)

def recipe_view(request, recipe_id):

    recipe = get_object_or_404(Recipe.objects.select_related('author').prefetch_related(
        'tags', 'ingredients', 'ingredientquantity_set'), pk=recipe_id)
    ingredients = zip(recipe.ingredients.all(),
                      recipe.ingredientquantity_set.all())

    return render(request, 'single_page.html', context={'recipe': recipe, 'ingredients': ingredients})
