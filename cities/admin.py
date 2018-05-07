from django.contrib import admin
from .models import Countries, Cities, Regions

class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Countries, AuthorAdmin)
admin.site.register(Regions, AuthorAdmin)
admin.site.register(Cities, AuthorAdmin)