from django.contrib import admin

from .models import Category, Comment, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
    )
    list_filter = ('is_published',)
    search_fields = ('title', 'slug',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )
    list_filter = ('is_published',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at',
    )
    list_filter = (
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
    )  
    search_fields = ('title',)
    empty_value_display = 'Не задано'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'created_at',
        'author',
    )
    search_fields = ('text',)
    list_filter = ('post', 'author',)
