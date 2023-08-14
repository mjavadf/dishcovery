from django.contrib import admin
from .models import User

# register user model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email']
