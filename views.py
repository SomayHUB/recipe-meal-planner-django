from collections import defaultdict
from datetime import date, timedelta

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MealPlanForm, RecipeForm
from .models import MealPlan, Recipe


def dashboard(request):
    recipes = Recipe.objects.all()
    upcoming = MealPlan.objects.select_related('recipe').filter(date__gte=date.today()).order_by('date', 'meal_type')[:8]
    context = {
        'recipe_count': recipes.count(),
        'favorite_count': recipes.filter(is_favorite=True).count(),
        'planned_count': MealPlan.objects.filter(date__gte=date.today()).count(),
        'upcoming': upcoming,
        'recent_recipes': recipes[:6],
    }
    return render(request, 'planner/dashboard.html', context)


def recipe_list(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    recipes = Recipe.objects.all()
    if query:
        recipes = recipes.filter(Q(name__icontains=query) | Q(ingredients__icontains=query))
    if category:
        recipes = recipes.filter(category=category)
    return render(request, 'planner/recipe_list.html', {
        'recipes': recipes,
        'query': query,
        'category': category,
        'categories': Recipe.CATEGORY_CHOICES,
    })


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'planner/recipe_detail.html', {'recipe': recipe})


def recipe_create(request):
    form = RecipeForm(request.POST or None)
    if form.is_valid():
        recipe = form.save()
        messages.success(request, f'{recipe.name} was added.')
        return redirect('planner:recipe_detail', pk=recipe.pk)
    return render(request, 'planner/recipe_form.html', {'form': form, 'title': 'Add Recipe'})


def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    form = RecipeForm(request.POST or None, instance=recipe)
    if form.is_valid():
        form.save()
        messages.success(request, 'Recipe updated successfully.')
        return redirect('planner:recipe_detail', pk=recipe.pk)
    return render(request, 'planner/recipe_form.html', {'form': form, 'title': 'Edit Recipe'})


def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        name = recipe.name
        recipe.delete()
        messages.success(request, f'{name} was deleted.')
        return redirect('planner:recipe_list')
    return render(request, 'planner/recipe_confirm_delete.html', {'recipe': recipe})


def toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.is_favorite = not recipe.is_favorite
        recipe.save(update_fields=['is_favorite'])
    return redirect(request.POST.get('next') or 'planner:recipe_list')


def meal_plan(request):
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    week_dates = [monday + timedelta(days=i) for i in range(7)]
    plans = MealPlan.objects.select_related('recipe').filter(date__range=(week_dates[0], week_dates[-1]))
    by_date = defaultdict(list)
    for plan in plans:
        by_date[plan.date].append(plan)
    return render(request, 'planner/meal_plan.html', {'week_dates': week_dates, 'plans': by_date})


def meal_plan_create(request):
    form = MealPlanForm(request.POST or None)
    if form.is_valid():
        plan = form.save(commit=False)
        existing = MealPlan.objects.filter(date=plan.date, meal_type=plan.meal_type).exclude(pk=plan.pk).first()
        if existing:
            form.add_error(None, 'That meal slot is already planned. Choose another meal type or date.')
        else:
            plan.save()
            messages.success(request, 'Meal added to your plan.')
            return redirect('planner:meal_plan')
    return render(request, 'planner/meal_plan_form.html', {'form': form})


def meal_plan_delete(request, pk):
    plan = get_object_or_404(MealPlan, pk=pk)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Meal removed from the plan.')
    return redirect('planner:meal_plan')


def shopping_list(request):
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    plans = MealPlan.objects.select_related('recipe').filter(date__range=(monday, sunday))
    items = []
    for plan in plans:
        for ingredient in plan.recipe.ingredient_list:
            items.append((ingredient, plan.recipe.name))
    return render(request, 'planner/shopping_list.html', {
        'items': items,
        'monday': monday,
        'sunday': sunday,
        'meal_count': plans.count(),
    })
