from django.contrib import admin
from .models import pro


class NaviAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'url',
        ]


admin.site.register(pro, NaviAdmin)

