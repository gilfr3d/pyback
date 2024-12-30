from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Fields', {
                'fields': ('role', 'mobile', ),
            },
        ),
    )
    list_display = ['username', 'email', 'role', 'mobile'] 

admin.site.register(CustomUser, CustomUserAdmin)
