from django.contrib import admin
from .models import BlogPost, Category, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'author', 'status', 'is_featured', 'created_at')
    list_filter = ('status', 'is_featured', 'company', 'category', 'created_at')
    search_fields = ('title', 'content', 'company__name', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'
    readonly_fields = ('views_count', 'likes_count', 'created_at', 'updated_at')
