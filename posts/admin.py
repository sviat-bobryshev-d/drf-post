from django.contrib import admin

from posts.models import Category, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content")
    list_display_links = ("id", "title")
    search_fields = ("title", "content")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("tag", "name")
    list_display_links = ("tag", "name")
    search_fields = ("tag", "name")

    class Meta:
        plural = "Categories"


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
