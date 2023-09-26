from .models import Post
from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content")
    list_display_links = ("id", "title")
    search_fields = ("title", "content")


admin.site.register(Post, PostAdmin)
