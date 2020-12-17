from django.shortcuts import render
from django.core.paginator import Paginator


from .models import (Recipe, Tag)


def index(request):

    tags = Tag.objects.all()

    recipes = Recipe.objects.select_related('author').prefetch_related('tags').all()
    paginator = Paginator(recipes, 1)
    
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    context = {'page': page, 'paginator': paginator, 'tags': tags}
    return render(request, 'index.html', context=context)
