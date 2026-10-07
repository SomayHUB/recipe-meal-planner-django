from datetime import date, timedelta
from django.core.management.base import BaseCommand
from planner.models import MealPlan, Recipe


RECIPES = [
    {
        'name': 'Masala Omelette', 'category': 'Breakfast', 'prep_minutes': 10, 'servings': 2, 'calories': 280,
        'ingredients': '4 eggs\n1 small onion\n1 tomato\n1 green chilli\n1 tbsp coriander\n1 tsp oil\nSalt to taste',
        'instructions': 'Beat eggs with salt. Mix in chopped onion, tomato, chilli and coriander. Heat oil, pour the mixture in, cook both sides and serve hot.', 'is_favorite': True,
    },
    {
        'name': 'Chickpea Power Bowl', 'category': 'Lunch', 'prep_minutes': 20, 'servings': 2, 'calories': 420,
        'ingredients': '1 cup cooked chickpeas\n1 cup cooked rice\n1 cucumber\n1 tomato\n1/2 cup curd\n1 tsp lemon juice\nChaat masala',
        'instructions': 'Arrange rice, chickpeas and chopped vegetables in bowls. Add curd, lemon juice and chaat masala. Mix before eating.', 'is_favorite': True,
    },
    {
        'name': 'Paneer Tikka Wrap', 'category': 'Dinner', 'prep_minutes': 25, 'servings': 2, 'calories': 510,
        'ingredients': '200 g paneer\n2 whole wheat rotis\n1 capsicum\n1 onion\n1/2 cup curd\n1 tsp tikka masala\n1 tsp oil',
        'instructions': 'Marinate paneer and vegetables in curd and tikka masala. Pan-cook until lightly charred. Fill rotis, roll and serve.', 'is_favorite': False,
    },
    {
        'name': 'Fruit Yogurt Cup', 'category': 'Snack', 'prep_minutes': 5, 'servings': 2, 'calories': 190,
        'ingredients': '1 cup yogurt\n1 banana\n1 apple\n1 tbsp oats\n1 tsp honey',
        'instructions': 'Chop fruit. Layer yogurt, fruit and oats in cups. Drizzle with honey and chill for a few minutes.', 'is_favorite': False,
    },
    {
        'name': 'Vegetable Poha', 'category': 'Breakfast', 'prep_minutes': 15, 'servings': 2, 'calories': 320,
        'ingredients': '2 cups poha\n1 onion\n1/2 cup peas\n1/2 tsp mustard seeds\n1 tbsp peanuts\n1 tsp oil\nTurmeric and salt',
        'instructions': 'Rinse poha and drain. Temper mustard seeds in oil, add onion, peas and peanuts. Add turmeric and poha, mix and cook for 3 minutes.', 'is_favorite': False,
    },
]


class Command(BaseCommand):
    help = 'Load sample recipes and a current-week meal plan.'

    def handle(self, *args, **options):
        recipes = {}
        for data in RECIPES:
            recipe, _ = Recipe.objects.update_or_create(name=data['name'], defaults=data)
            recipes[recipe.name] = recipe

        monday = date.today() - timedelta(days=date.today().weekday())
        plan_data = [
            (0, 'Breakfast', 'Masala Omelette'),
            (0, 'Lunch', 'Chickpea Power Bowl'),
            (1, 'Breakfast', 'Vegetable Poha'),
            (2, 'Dinner', 'Paneer Tikka Wrap'),
            (3, 'Snack', 'Fruit Yogurt Cup'),
            (4, 'Lunch', 'Chickpea Power Bowl'),
        ]
        for offset, meal_type, recipe_name in plan_data:
            MealPlan.objects.update_or_create(
                date=monday + timedelta(days=offset),
                meal_type=meal_type,
                defaults={'recipe': recipes[recipe_name]},
            )
        self.stdout.write(self.style.SUCCESS('Sample recipes and meal plan loaded successfully.'))
