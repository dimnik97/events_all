from django.contrib import admin
from .models import Profile

class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profile, AuthorAdmin)