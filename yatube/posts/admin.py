from django.contrib import admin

from .models import Post, Group, Follow, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Админка для Post."""
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Админка для Group."""


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Админка для Follow."""


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка для Comment."""
