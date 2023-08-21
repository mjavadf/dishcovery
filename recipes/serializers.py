from rest_framework import serializers
from .models import Profile, Recipe, Ingredient, RecipeIngredient, Comment


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
        fields = ["id", "name", "amount", "unit", "image"]


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSimpleSerializer(many=True)
    
    class Meta:
        model = Recipe
        fields = [
            "id",
            "user",
            "title",
            "time_minutes",
            "description",
            "image",
            "created_at",
            "modified_at",
            "ingredients",
        ]


class IngredientSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ingredient
        fields = ["id", "name", "image", "created_at", "modified_at", "created_by"]

    def create(self, validated_data):
        return super().create(validated_data, created_by=self.context["user"])


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "recipe",
            "comment",
            "created_at",
            "modified_at",
        ]

    def create(self, validated_data):
        recipe_id = self.context["recipe_id"]
        user = self.context["request"].user
        return Comment.objects.create(recipe_id=recipe_id, user=user, **validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Profile
        fields = ["id", "user", "image", "bio",]