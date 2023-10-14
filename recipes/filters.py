from django_filters import rest_framework as filters
from .models import Recipe

class RecipeFilter(filters.FilterSet):
    """
    A filter set for Recipe model.

    Available filters:
    - ingredients__ingredient__name: exact match for ingredient name
    - time_minutes: exact match, less than or equal, greater than or equal
    - user__username: exact match for username
    """
    class Meta:
        model = Recipe
        fields = {
            "ingredients__ingredient__name": ["iexact"],
            "time_minutes": ["exact", "lte", "gte"],
            "user__username": ["iexact"],
        }