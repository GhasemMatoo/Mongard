from django.contrib import admin
from .models import Post, Comment, Vote
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'slug', 'updated']
    search_fields = ('slug', 'user__username')
    prepopulated_fields = {'slug': ('user', 'body')}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created', 'is_reply']
    raw_id_fields = ['user', 'post', 'replay']


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Vote)
