from django.contrib import admin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('name', 'updated_at', 'created_at')
    search_fields = ('name', 'updated_at', 'created_at')