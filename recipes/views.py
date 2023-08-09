from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer
from .permissions import IsAuthenticatedOrReadOnly, IsOwner


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_permissions(self):
        match self.action:
            case "create":
                permission_classes = [IsAuthenticated]
            case "update" | "partial_update" | "destroy":
                permission_classes = [IsOwner]
            case "retrieve" | "list":
                permission_classes = []
            case _:
                permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request"] = self.request
        return context


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_context_data(self, **kwargs):
        context = {"user": self.request.user}
        return context
