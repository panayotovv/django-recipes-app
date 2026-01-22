from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView
from Recipes.forms import CustomUserCreationForm, CustomEditForm, ProfileForm, ProfileImageForm
from Recipes.models import Recipe, RecipeIngredient


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["favorite_recipes"] = user.favorite_recipes.all()

        profile = getattr(user, 'profile', None)
        if profile and profile.profile_picture:
            picture_url = profile.profile_picture.url
        else:
            picture_url = settings.MEDIA_URL + "default.jpg"

        context["profile_picture_url"] = picture_url

        return context

class IndexView(ListView):
    model = Recipe
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.all()[:3]
        return context

class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

class RecipesView(ListView):
    model = Recipe
    template_name = 'recipes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.all()
        return context

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe-details.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = RecipeIngredient.objects.filter(recipe=self.object)
        return context


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()

        user = authenticate(
            username=user.username,
            password=form.cleaned_data['password1']
        )

        if user is not None:
            login(self.request, user)

        return redirect(self.get_success_url())


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm

class EditProfileView(LoginRequiredMixin, View):
    template_name = "edit.html"

    def get(self, request):
        user = request.user
        profile = user.profile

        user_form = CustomEditForm(instance=user)
        profile_form = ProfileForm(instance=profile)

        return render(request, self.template_name, {
            "user_form": user_form,
            "profile_form": profile_form
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile

        if "profile_picture" in request.FILES:
            form = ProfileImageForm(
                request.POST,
                request.FILES,
                instance=profile
            )
            if form.is_valid():
                form.save()
            return redirect("profile")

        user_form = CustomEditForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")

        return render(request, self.template_name, {
            "user_form": user_form,
            "profile_form": profile_form,
        })


@login_required
def toggle_favorite(request, recipe_id):
    user = request.user
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return JsonResponse({"error": "Recipe not found"}, status=404)

    if user in recipe.favorited_by.all():
        recipe.favorited_by.remove(user)
        liked = False
    else:
        recipe.favorited_by.add(user)
        liked = True

    return JsonResponse({"liked": liked})



