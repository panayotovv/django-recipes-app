from rest_framework import serializers
from .models import Recipe, Ingredient, RecipeIngredient, Instructions


class InstructionsSerializer(serializers.ModelSerializer):
    recipe = serializers.CharField(source='recipe.title')
    instructions = serializers.CharField(source='text')

    class Meta:
        model = Instructions
        fields = ['id', 'recipe', 'instructions']

class IngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.CharField(source='name')

    class Meta:
        model = Ingredient
        fields = ['id', 'ingredient']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(write_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['name', 'ingredient_name', 'quantity', 'unit']

    def create(self, validated_data):
        ingredient_name = validated_data.pop('ingredient_name')
        ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
        return RecipeIngredient.objects.create(ingredient=ingredient, **validated_data)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set',
        many=True
    )
    instructions = InstructionsSerializer()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'prep_time',
            'cook_time',
            'description',
            'instructions',
            'ingredients'
        ]


    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set')
        instructions_data = validated_data.pop('instructions')
        instructions = Instructions.objects.create(**instructions_data)

        recipe = Recipe.objects.create(instructions=instructions, **validated_data)


        for item in ingredients_data:
            RecipeIngredientSerializer().create({**item, 'recipe': recipe})

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set', None)
        instructions_data = validated_data.pop('instructions', None)

        instance = super().update(instance, validated_data)

        if instructions_data:
            for attr, value in instructions_data.items():
                setattr(instance.instructions, attr, value)
            instance.instructions.save()

        if ingredients_data is not None:
            instance.recipeingredient_set.all().delete()

            for item in ingredients_data:
                RecipeIngredientSerializer().create({
                    **item,
                    'recipe': instance
                })

        return instance


