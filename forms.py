from django import forms
from .models import MealPlan, Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'category', 'prep_minutes', 'servings', 'calories', 'ingredients', 'instructions', 'is_favorite']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 6, 'placeholder': '2 eggs\n1 tomato\n1 tsp oil'}),
            'instructions': forms.Textarea(attrs={'rows': 6, 'placeholder': '1. Chop the vegetables.\n2. Cook and serve.'}),
        }


class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ['date', 'meal_type', 'recipe', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
