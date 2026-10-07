from datetime import date
from django.test import TestCase
from django.urls import reverse
from .models import MealPlan, Recipe


class PlannerTests(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name='Test Salad', category='Lunch', prep_minutes=10, servings=1, calories=200,
            ingredients='1 tomato\n1 cucumber', instructions='Chop and mix.'
        )

    def test_recipe_list_page(self):
        response = self.client.get(reverse('planner:recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Salad')

    def test_create_recipe(self):
        response = self.client.post(reverse('planner:recipe_create'), {
            'name': 'New Recipe', 'category': 'Dinner', 'prep_minutes': 20,
            'servings': 2, 'calories': 350, 'ingredients': 'Rice',
            'instructions': 'Cook rice.', 'is_favorite': 'on'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipe.objects.filter(name='New Recipe').exists())

    def test_meal_plan_unique_slot(self):
        MealPlan.objects.create(date=date.today(), meal_type='Lunch', recipe=self.recipe)
        self.assertEqual(MealPlan.objects.count(), 1)
