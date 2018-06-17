from django.contrib import admin
from .models import Profile, ProfileAvatar, UserSettings


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, AuthorAdmin)
admin.site.register(ProfileAvatar, AuthorAdmin)
admin.site.register(UserSettings, AuthorAdmin)