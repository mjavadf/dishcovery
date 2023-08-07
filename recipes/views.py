from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Recipe, Ingredient
from .serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request"] = self.request
        return context
