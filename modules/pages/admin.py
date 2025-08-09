from django.contrib import admin
from .models import Page

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'author', 'is_published', 'created_at')
    list_filter = ('is_published', 'company', 'created_at')
    search_fields = ('title', 'content', 'company__name', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
