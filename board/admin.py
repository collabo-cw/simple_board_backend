from django.contrib import admin

from board.models import Board


# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass