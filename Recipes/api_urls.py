from django.urls import path
from Recipes.views import RecipeListCreate, RecipeRetrieveUpdateDestroy, InstructionsList, \
    InstructionsRetrieveUpdateDestroy, IngredientListCreate, IngredientsRetrieveUpdateDestroy

urlpatterns = [
    path('recipes/', RecipeListCreate.as_view(), name='recipe_create'),
    path('recipes/<int:pk>/', RecipeRetrieveUpdateDestroy.as_view(), name='recipe_update'),
    path('instructions/', InstructionsList.as_view(), name='instructions_create'),
    path('instructions/<int:pk>/', InstructionsRetrieveUpdateDestroy.as_view(), name='instructions_update'),
    path('ingredients/', IngredientListCreate.as_view(), name='ingredient_create'),
    path('ingredients/<int:pk>/', IngredientsRetrieveUpdateDestroy.as_view(), name='ingredient_update'),
]