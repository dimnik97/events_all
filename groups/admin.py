from django.contrib import admin

# Register your models here.
from cities.admin import AuthorAdmin
from groups.models import Group, GroupSubscribers

admin.site.register(Group, AuthorAdmin)
admin.site.register(GroupSubscribers, AuthorAdmin)