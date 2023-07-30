from django.contrib import admin
from . import models

class RecipeIngredientInline(admin.TabularInline):
    model = models.RecipeIngredient
    extra = 1

@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'modified_at']
    inlines = [RecipeIngredientInline]
    
@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at', 'modified_at']
