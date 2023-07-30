from django.contrib import admin
from .models import User

# register user model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'date_joined']
