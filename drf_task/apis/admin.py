from django.contrib import admin
from .models import User, Blog, Article
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
   list_display = ['id', 'name', 'email']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
   list_display = ['title', 'author']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
   list_display = ['title', 'blog', 'author']

