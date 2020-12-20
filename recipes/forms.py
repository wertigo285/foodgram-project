from django.forms import ModelForm, MultipleChoiceField

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'duration', 'description', 'image')
