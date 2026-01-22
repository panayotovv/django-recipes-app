from django.contrib.auth.views import LogoutView
from django.urls import path

from Recipes import views
from Recipes.views import IndexView, AboutView, CustomLoginView, RegisterView, RecipesView, RecipeDetailView, \
    ProfileView, ContactView, EditProfileView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit'),
    path('recipes/', RecipesView.as_view(), name='recipes'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),

    path('recipe/<int:recipe_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='home'), name="logout"),
]