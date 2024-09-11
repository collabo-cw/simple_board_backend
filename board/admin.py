from django.contrib import admin

from board.models import Board


# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    model = Board
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('title', 'author', 'created_at', 'updated_at')