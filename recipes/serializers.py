from rest_framework import serializers
from .models import Profile, Recipe, Ingredient, RecipeIngredient, Comment


class RecipeIngredientSimpleSerializer(serializers.ModelSerializer):
    """
    A serializer for the RecipeIngredient model that returns a simplified representation of the ingredient.

    The serializer includes the ingredient's ID, name, amount, unit, and image. If a custom name or image is available,
    it will be used instead of the default values.

    Methods:
    - get_name: Returns the ingredient's custom name if available, otherwise returns the default name.
    - get_image: Returns the ingredient's custom image if available, otherwise returns the default image.
    """

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
    """
    Serializer for the Recipe model. Includes nested serialization for RecipeIngredientSimpleSerializer.
    """
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
    """
    Serializer for Ingredient model.
    """
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ingredient
        fields = ["id", "name", "image", "created_at", "modified_at", "created_by"]

    def create(self, validated_data):
        """
        Create a new ingredient instance.

        Args:
            validated_data (dict): The validated data for the new ingredient.

        Returns:
            Ingredient: The newly created ingredient instance.
        """
        return super().create(validated_data, created_by=self.context["user"])


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.

    Fields:
    - id: The ID of the comment.
    - user: The user who created the comment.
    - recipe: The recipe the comment belongs to.
    - comment: The comment text.
    - created_at: The date and time the comment was created.
    - modified_at: The date and time the comment was last modified.

    Methods:
    - create: Creates a new comment instance.
    """
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
    """
    Serializer for the Profile model.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Profile
        fields = ["id", "user", "image", "bio", "phone_number",]