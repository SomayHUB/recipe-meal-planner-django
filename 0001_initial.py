from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('category', models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snack', 'Snack')], max_length=20)),
                ('prep_minutes', models.PositiveIntegerField(default=15)),
                ('servings', models.PositiveIntegerField(default=2)),
                ('ingredients', models.TextField(help_text='One ingredient per line, e.g. 2 eggs')),
                ('instructions', models.TextField()),
                ('calories', models.PositiveIntegerField(default=0)),
                ('is_favorite', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='MealPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('meal_type', models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snack', 'Snack')], max_length=20)),
                ('notes', models.CharField(blank=True, max_length=200)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meal_plans', to='planner.recipe')),
            ],
            options={'ordering': ['date', 'meal_type']},
        ),
        migrations.AddConstraint(
            model_name='mealplan',
            constraint=models.UniqueConstraint(fields=('date', 'meal_type'), name='unique_meal_per_day_type'),
        ),
    ]
