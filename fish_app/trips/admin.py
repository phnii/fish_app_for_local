from django.contrib import admin
from .models import Trip, Result, Comment

class PostInline(admin.TabularInline):
    model = Result

class CommentInline(admin.TabularInline):
    model = Comment

class TripAdmin(admin.ModelAdmin):
    inlines = [
        PostInline,
        CommentInline,
    ]
    list_display = ('title', 'content', 'user')

admin.site.register(Trip, TripAdmin)