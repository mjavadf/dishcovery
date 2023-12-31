from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import Profile, Recipe, Ingredient, Comment
from .serializers import CommentSerializer, ProfileSerializer, RecipeCreateSerializer, RecipeSerializer, IngredientSerializer
from .permissions import IsAuthenticatedOrReadOnly, IsOwner
from .filters import RecipeFilter
from .pagination import DefaultPagination


class RecipeViewSet(ModelViewSet):
    # prefetch_related() is used to reduce the number of queries made to the database.
    queryset = Recipe.objects.prefetch_related('ingredients').all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RecipeFilter
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "time_minutes"]
    pagination_class = DefaultPagination

    def get_permissions(self):
        # The permissions are determined by the action being performed.
        match self.action:
            case "create":
                # Only authenticated users can create recipes.
                permission_classes = [IsAuthenticated]
            case "update" | "partial_update" | "destroy":
                # Only the recipe's owner or an admin can update or delete a recipe.
                permission_classes = [IsOwner]
            case "retrieve" | "list":
                # Anyone can view a recipe.
                permission_classes = []
            case _:
                # Only authenticated users can perform other actions.
                permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        match self.action:
            case "create" | "update" | "partial_update":
                serializer_class = RecipeCreateSerializer
            case _:
                serializer_class = RecipeSerializer
        
        return serializer_class

    def get_context_data(self, **kwargs):
        ontext = {"request": self.request}
        return context


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination

    def get_context_data(self, **kwargs):
        context = {"request": self.request}
        return context


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_context(self):
        return {"request": self.request,
                "recipe_id": self.kwargs["recipe_pk"],}
    
    def get_queryset(self):
        return Comment.objects.filter(recipe_id=self.kwargs["recipe_pk"])
    
    def get_permissions(self):
        match self.action:
            case "create":
                permission_classes = [IsAuthenticated]
            case "update" | "partial_update":
                permission_classes = [IsOwner]
            case "retrieve" | "list":
                permission_classes = []
            case "destroy":
                permission_classes = [IsOwner | IsAdminUser]
            case _:
                permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    
    
class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def get_permissions(self):
        match self.action:
            case "update" | "partial_update":
                permission_classes = [IsOwner]
            case 'me':
                permission_classes = [IsAuthenticated]
            case _:
                permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        profile = Profile.objects.get(user_id=request.user.id)
        if request.method == "GET":
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        else:
            serializer = ProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)