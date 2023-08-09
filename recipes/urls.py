from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('recipes', views.RecipeViewSet, basename='recipes')
router.register('ingredients', views.IngredientViewSet, basename='ingredients')

recipe_router = routers.NestedDefaultRouter(router, 'recipes', lookup='recipe')
recipe_router.register('comments', views.CommentViewSet, basename='recipe-comments')

urlpatterns = router.urls + recipe_router.urls