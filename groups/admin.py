from django.contrib import admin

from groups.models import Group, AllRoles, Membership, GroupAvatar

admin.site.register(Group)
admin.site.register(AllRoles)
admin.site.register(Membership)
admin.site.register(GroupAvatar)