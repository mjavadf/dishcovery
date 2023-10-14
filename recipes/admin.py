from django.contrib import admin
from django.utils.html import format_html
from . import models


class RecipeIngredientInline(admin.StackedInline):
    """
    Inline admin class for RecipeIngredient model.
    """
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
        """
        Returns the thumbnail image for the RecipeIngredient object.
        If a custom image is provided, it will be used, otherwise the ingredient's image will be used.
        """
        if obj.custom_image.name != "":
            return format_html(
                f'<img src="{obj.custom_image.url}" style="max-width: 200px; max-height: 200px; object-fit: cover;" />'
            ) 
        return format_html(
            f'<img src="{obj.ingredient.image.url}" style="max-width: 200px; max-height: 200px; object-fit: cover;" />'
        )


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Admin class for Recipe model.
    """
    list_display = ["title", "user", "created_at", "modified_at"]
    inlines = [RecipeIngredientInline]


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Admin class for Ingredient model.
    """
    list_display = ["name", "created_by", "created_at", "modified_at"]
    search_fields = ["name"]
    readonly_fields = ["thumbnail"]

    def thumbnail(self, obj):
        """
        Returns the thumbnail image for the ingredient object.

        Args:
            obj: The Ingredient object.

        Returns:
            The HTML code for the thumbnail image.
        """
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
    

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin class for the Profile model.

    Attributes:
        list_select_related (list): List of related fields to select.
        list_display (list): List of fields to display in the list view.
        readonly_fields (list): List of fields that are read-only.
        search_fields (list): List of fields to search for.
        list_filter (list): List of fields to filter by.
        ordering (list): List of fields to order by.
        autocomplete_fields (list): List of fields to autocomplete.
    """
    list_select_related = ["user"]
    list_display = ["first_name", "last_name", "phone_number", "created_at", "modified_at"]
    readonly_fields = ["thumbnail", "created_at", "modified_at"]
    search_fields = ["user__username"]
    list_filter = ["created_at", "modified_at"]
    ordering = ["user__first_name", "user__last_name"]
    autocomplete_fields = ["user"]
    
    def thumbnail(self, obj):
        if obj.image.name != "":
            return format_html(
                f'<img src="{obj.image.url}" style="max-width: 200px; max-height: 200px; object-fit: cover;" />'
            )
        return "No image"