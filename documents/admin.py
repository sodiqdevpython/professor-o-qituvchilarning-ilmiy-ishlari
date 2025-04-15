from django.contrib import admin
from .models import DocumentType, DocumentTypeSubtitles, Document, Requirements

@admin.register(DocumentTypeSubtitles)
class DocumentTypeSubtitlesAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'subtitle', 'created', 'updated')
    list_filter = ('subtitle',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'author', 'created', 'updated')
    list_filter = ('type', 'author')
    search_fields = ('name', 'author__first_name', 'author__last_name')
    ordering = ('created',)

    readonly_fields = ('created', 'updated')

    fieldsets = (
        (None, {'fields': ('name', 'type', 'author', 'file', 'url', 'image')}),
        ('Metadata', {'fields': ('created', 'updated')}),
    )

@admin.register(Requirements)
class RequirementsAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'numbers', 'created', 'updated')
    list_filter = ('document_type', 'user')
    search_fields = ('user__first_name', 'user__last_name', 'document_type__name')
    ordering = ('created',)
