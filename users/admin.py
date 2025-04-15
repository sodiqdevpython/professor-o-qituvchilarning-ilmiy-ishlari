from django.contrib import admin
from .models import User, Faculty

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'tel_number', 'type', 'faculty', 'is_active')
    list_filter = ('type', 'is_active', 'faculty')
    search_fields = ('first_name', 'last_name', 'email', 'tel_number')
    ordering = ('first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email')}),
        ('Contact Info', {'fields': ('tel_number',)}),
        ('Permissions', {'fields': ('type', 'faculty', 'is_active', 'is_staff', 'is_superuser')}),
    )

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin')
    search_fields = ('name',)
