from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'author')
    list_filter = ['date_posted']
    search_fields = ['title']


admin.site.register(Post, PostAdmin)
