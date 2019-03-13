from django.contrib import admin
import datetime

from forum.models import *
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'date', 'thread')


admin.site.register(Post, PostAdmin)


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title', 'forum', )}


admin.site.register(Thread, ThreadAdmin)


class ForumAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Forum, ForumAdmin)
