from rest_framework import serializers
from .models import Recipe, Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            "user",
            "title",
            "time_minutes",
            "description",
            "image",
            "created_at",
            "modified_at",
            "ingredients",
        ]
