from django_filters import rest_framework as filters
from .models import Recipe

class RecipeFilter(filters.FilterSet):
    class Meta:
        model = Recipe
        fields = {
            "ingredients__ingredient__name": ["iexact"],
            "time_minutes": ["exact", "lte", "gte"],
            "user__username": ["iexact"],
        }