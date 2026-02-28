from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from Recipes.models import Profile, Recipe, Instructions, RecipeIngredient, Ingredient
import uuid

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        user.username = str(uuid.uuid4())[:150]

        if commit:
            user.save()
            Profile.objects.get_or_create(user=user)

        return user


class CustomLoginForm(AuthenticationForm):
    pass

class RecipeAddForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['ingredients', 'instructions', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none'}),
            'image': forms.FileInput(attrs={'class': 'hidden', 'id': 'image-upload'}),
            'prep_time': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none'}),
            'cook_time': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none'}),
            'description': forms.Textarea(attrs={'rows': 1, 'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none'}),
            'ingredients': forms.Textarea(attrs={'rows': 2,'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none'}),
            'instructions': forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none'}),
        }

class InstructionsForm(forms.ModelForm):
    class Meta:
        model = Instructions
        fields = '__all__'
        widgets = {
            'text': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none'}),
        }


class RecipeIngredientForm(forms.ModelForm):
    ingredient_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'w-full px-4 py-2 border rounded-lg'}
        )
    )

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient_name', 'quantity', 'unit']
        widgets = {
            'ingredient_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'unit': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
        }

    def save(self, commit=True):
        ingredient_name = self.cleaned_data['ingredient_name']

        ingredient, _ = Ingredient.objects.get_or_create(
            name=ingredient_name.strip().lower()
        )

        self.instance.ingredient = ingredient
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return super().save(commit=commit)


RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=1,
)

class CustomEditForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none'
        }),
        help_text="Leave blank if you don't want to change the password."
    )

    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none'
        }),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password:
            if password != confirm_password:
                raise ValidationError("Passwords do not match.")

            validate_password(password)

        return cleaned_data



class ProfileForm(forms.ModelForm):
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none'
        })
    )

    class Meta:
        model = Profile
        fields = ['bio']


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_picture"]
