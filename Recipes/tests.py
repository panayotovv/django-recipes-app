from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Recipe, Instructions, Ingredient, RecipeIngredient

class RecipeTest(TestCase):
    def setUp(self):
        self.user, created = User.objects.get_or_create(username="tester")

        self.instructions = Instructions.objects.create(text="Step 1: Do this")

        self.ingredient, created = Ingredient.objects.get_or_create(name="Salt")

        self.image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            prep_time=10,
            cook_time=20,
            description="Delicious recipe",
            instructions=self.instructions,
            image=self.image,
            author=self.user
        )

        RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=100,
            unit='g',
        )

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.title, "Test Recipe")
        self.assertEqual(self.recipe.prep_time, 10)
        self.assertEqual(self.recipe.cook_time, 20)
        self.assertIn(self.ingredient, self.recipe.ingredients.all())
        self.assertEqual(self.recipe.author, self.user)
