# Recipe Meal Planner using Django

A practical Django implementation inspired by the **Recipe Meal Planner** project listed in the GeeksforGeeks Django Projects collection. The application was designed from scratch as a student project rather than copying the source implementation.

## Features

- Add, edit, view and delete recipes
- Search recipes by name or ingredient
- Filter recipes by meal category
- Mark recipes as favorites
- Weekly meal planner with breakfast, lunch, dinner and snack slots
- Prevent duplicate meal types on the same date
- Automatically generate a weekly shopping list from planned recipes
- Django admin panel for managing recipes and meal plans
- SQLite database for simple local development
- Seed command with realistic sample data
- Automated tests for core functionality
- Responsive UI using plain HTML/CSS and Django templates

## Tech Stack

- Python 3.11+
- Django 5.2
- SQLite
- HTML5 / CSS3
- Django Templates

## Project Structure

```text
recipe_meal_planner/
├── manage.py
├── requirements.txt
├── README.md
├── mealplanner/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── planner/
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── tests.py
    ├── migrations/
    ├── management/commands/seed_data.py
    ├── templates/planner/
    └── static/planner/style.css
```

## How to Run

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply migrations

```bash
python manage.py migrate
```

### 4. Load sample data

```bash
python manage.py seed_data
```

### 5. Run the server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Admin Panel

Create an admin account:

```bash
python manage.py createsuperuser
```

Then open `http://127.0.0.1:8000/admin/`.

## Tests

```bash
python manage.py test
```

## Demo Flow

1. Open the dashboard and show recipe/meal statistics.
2. Open **Recipes** and search for `paneer`.
3. Open a recipe and explain its model data, ingredients and instructions.
4. Add a new recipe using the form.
5. Open **Meal Planner** and show the seeded current-week meals.
6. Add another meal and demonstrate the duplicate-slot validation.
7. Open **Shopping List** and explain that it is generated from the current week's planned recipes.
8. Open `/admin/` to demonstrate Django's built-in admin interface.

## Viva / Explanation Points

### MVT architecture

- **Models:** `Recipe` and `MealPlan` define the database structure.
- **Views:** `planner/views.py` handles requests, filtering, CRUD operations and shopping-list generation.
- **Templates:** HTML files under `planner/templates/planner/` render the UI.

### Important relationship

`MealPlan.recipe` is a `ForeignKey` to `Recipe`. This means one recipe can be used in many meal-plan entries, while each meal-plan entry points to one recipe.

### Why SQLite?

SQLite is Django's default lightweight database and is convenient for a classroom/local project. The models can later be moved to PostgreSQL or MySQL by changing database configuration.

### Shopping list logic

The shopping-list view gets the current week's `MealPlan` objects, follows each meal's related `Recipe`, splits its ingredient text into individual lines, and displays the combined items.

## Reference

The project was selected from the GeeksforGeeks Django Projects collection, where **Recipe Meal Planner using Django** is listed among the beginner Django projects.
