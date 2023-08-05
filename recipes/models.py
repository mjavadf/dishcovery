from django.db import models
from django.conf import settings

user = settings.AUTH_USER_MODEL

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='images/ingredients/')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(user, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
    

class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        user,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='images/recipes/')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="recipes")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    custom_name = models.CharField(max_length=255, blank=True, null=True)
    custom_image = models.ImageField(upload_to='images/ingredients/', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.ingredient.name} ({self.amount} {self.unit})"
    
    class Meta:
        verbose_name = 'Recipe Ingredient'
        verbose_name_plural = 'Recipe Ingredients'
