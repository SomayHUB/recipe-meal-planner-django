from django.contrib import admin
from .models import MealPlan, Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'prep_minutes', 'servings', 'calories', 'is_favorite')
    list_filter = ('category', 'is_favorite')
    search_fields = ('name', 'ingredients')


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('date', 'meal_type', 'recipe', 'notes')
    list_filter = ('meal_type', 'date')
