from django.contrib import admin

# Register your models here.
from cities.admin import AuthorAdmin
from groups.models import Group, AllRoles, Membership, GroupAvatar

admin.site.register(Group, AuthorAdmin)
admin.site.register(AllRoles, AuthorAdmin)
admin.site.register(Membership, AuthorAdmin)
admin.site.register(GroupAvatar, AuthorAdmin)