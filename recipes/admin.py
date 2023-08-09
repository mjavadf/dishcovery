from django.contrib import admin
from django.utils.html import format_html
from . import models


class RecipeIngredientInline(admin.StackedInline):
    model = models.RecipeIngredient
    autocomplete_fields = ["ingredient"]
    extra = 1
    fieldsets = [
        (
            None,
            {
                "fields": ["ingredient", "amount", "unit", "thumbnail"],
            },
        ),
        (
            "Optionals",
            {
                "classes": ["collapse"],
                "fields": ["custom_name", "custom_image"],
            },
        ),
    ]
    readonly_fields = ["thumbnail"]

    def thumbnail(self, obj):
        if obj.custom_image.name != "":
            return format_html(
                f'<img src="{obj.custom_image.url}" style="max-width: 200px; max-height: 200px; object-fit: cover;" />'
            ) 
        return format_html(
            f'<img src="{obj.ingredient.image.url}" style="max-width: 200px; max-height: 200px; object-fit: cover;" />'
        )


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "created_at", "modified_at"]
    inlines = [RecipeIngredientInline]


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "created_by", "created_at", "modified_at"]
    search_fields = ["name"]
    readonly_fields = ["thumbnail"]

    def thumbnail(self, obj):
        if obj.image.name != "":
            return format_html(
                f'<img src="{obj.image.url}" style="max-width: 200px; max-height: 200px; object-fit: cover;" />'
            )
        return "No image"


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "recipe", "created_at", "modified_at"]
    search_fields = ["user__username", "recipe__title"]
    readonly_fields = ["created_at", "modified_at"]