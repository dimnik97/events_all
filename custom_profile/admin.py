from django.contrib import admin
from .models import Profile, Subscribers, ProfileAvatar, UserSettings


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, AuthorAdmin)
admin.site.register(Subscribers, AuthorAdmin)
admin.site.register(ProfileAvatar, AuthorAdmin)
admin.site.register(UserSettings, AuthorAdmin)