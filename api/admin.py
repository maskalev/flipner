from django.contrib import admin

from .models import Book, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["column_name", "is_visible"]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "title", "author", "description", "price"]
    search_fields = ["name", "title", "author", "description"]
