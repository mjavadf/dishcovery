from django.db import models
from django.conf import settings
from django.contrib import admin

user = settings.AUTH_USER_MODEL

class Ingredient(models.Model):
    """
    A model representing an ingredient used in a recipe.

    Attributes:
        name (str): The name of the ingredient.
        image (ImageField): An image of the ingredient.
        created_at (DateTimeField): The date and time the ingredient was created.
        modified_at (DateTimeField): The date and time the ingredient was last modified.
        created_by (ForeignKey): The user who created the ingredient.
    """
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
    """
    A model representing a recipe.

    Attributes:
        user (ForeignKey): The user who created the recipe.
        title (CharField): The title of the recipe.
        time_minutes (IntegerField): The time required to prepare the recipe in minutes.
        description (TextField): The description of the recipe.
        image (ImageField): The image of the recipe.
        created_at (DateTimeField): The date and time when the recipe was created.
        modified_at (DateTimeField): The date and time when the recipe was last modified.
    """
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
    """
    A model representing an ingredient used in a recipe.

    Attributes:
        ingredient (ForeignKey): The ingredient used in the recipe.
        recipe (ForeignKey): The recipe that uses the ingredient.
        custom_name (CharField): A custom name for the ingredient (optional).
        custom_image (ImageField): An image of the ingredient (optional).
        amount (DecimalField): The amount of the ingredient used in the recipe.
        unit (CharField): The unit of measurement for the ingredient amount (optional).
    """
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="recipes")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    custom_name = models.CharField(max_length=255, blank=True, null=True)
    custom_image = models.ImageField(upload_to='images/ingredients/', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.ingredient.name} ({self.amount} {self.unit})"
    
    class Meta:
        verbose_name = 'Recipe Ingredient'
        verbose_name_plural = 'Recipe Ingredients'


class Comment(models.Model):
    """
    Model representing a comment on a recipe.

    Attributes:
        recipe (ForeignKey to Recipe): The recipe to which the comment belongs.
        user (ForeignKey to User): The user who wrote the comment.
        comment (TextField): The text content of the comment.
        created_at (DateTimeField): The timestamp indicating when the comment was created.
        modified_at (DateTimeField): The timestamp indicating when the comment was last modified.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        
        
class Profile(models.Model):
    """
    A model representing a user profile.

    Attributes:
        user (User): A one-to-one field to the User model.
        image (ImageField): An image field for the user's profile picture.
        bio (TextField): A text field for the user's bio.
        phone_number (CharField): A char field for the user's phone number.
        created_at (DateTimeField): A date time field for the creation date of the profile.
        modified_at (DateTimeField): A date time field for the last modification date of the profile.
    """
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name', description='First Name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name', description='Last Name')
    def last_name(self):
        return self.user.last_name
    
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'