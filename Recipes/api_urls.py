from django.urls import path
from Recipes.views import RecipeListCreate, RecipeRetrieveUpdateDestroy

urlpatterns = [
    path('recipes/', RecipeListCreate.as_view(), name='recipe_create'),
    path('recipes/<int:pk>/', RecipeRetrieveUpdateDestroy.as_view(), name='recipe_update')
]