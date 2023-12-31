from django.contrib import admin

from .models import CustomUser, Follow

admin.site.register(CustomUser)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
