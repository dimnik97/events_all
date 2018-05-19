from django.contrib import admin
from .models import Profile, Subscribers, Profile_avatar


class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profile, AuthorAdmin)
admin.site.register(Subscribers, AuthorAdmin)
admin.site.register(Profile_avatar, AuthorAdmin)