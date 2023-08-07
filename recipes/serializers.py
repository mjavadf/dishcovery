from rest_framework import serializers
from .models import Recipe, Ingredient, RecipeIngredient

class RecipeIngredientSimpleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name="get_name", read_only=True)
    image = serializers.SerializerMethodField(method_name="get_image", read_only=True)
    
    def get_name(self, obj):
        if obj.custom_name is not None:
            return obj.custom_name
        return obj.ingredient.name
    
    def get_image(self, obj):
        request = self.context.get("request")
        if obj.custom_image != "":
            return request.build_absolute_uri(obj.custom_image.url)
        return request.build_absolute_uri(obj.ingredient.image.url)
    
    class Meta:
        model = RecipeIngredient
        fields = ["name", "amount", "unit", "image"]


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSimpleSerializer(many=True)
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
