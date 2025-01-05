from django.contrib import admin
from .models import Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'slug', 'updated']
    search_fields = ('slug', 'user__username')
    prepopulated_fields = {'slug': ('user', 'body')}


admin.site.register(Post, PostAdmin)
