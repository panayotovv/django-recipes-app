from django.apps import AppConfig

class RecipesConfig(AppConfig):
    name = 'Recipes'

    def ready(self):
        import Recipes.signals