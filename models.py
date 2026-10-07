from django.db import models


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    ]

    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    prep_minutes = models.PositiveIntegerField(default=15)
    servings = models.PositiveIntegerField(default=2)
    ingredients = models.TextField(help_text='One ingredient per line, e.g. 2 eggs')
    instructions = models.TextField()
    calories = models.PositiveIntegerField(default=0)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def ingredient_list(self):
        return [line.strip() for line in self.ingredients.splitlines() if line.strip()]


class MealPlan(models.Model):
    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    ]

    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='meal_plans')
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['date', 'meal_type']
        constraints = [
            models.UniqueConstraint(fields=['date', 'meal_type'], name='unique_meal_per_day_type')
        ]

    def __str__(self):
        return f'{self.date} - {self.meal_type} - {self.recipe.name}'
