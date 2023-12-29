from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = [
        'email',
        'is_active',
    ]

    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            _("Personal info"),
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "groups",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "groups",
                ),
            },
        ),
    )

    filter_horizontal = tuple()

    list_filter = ('is_staff', 'is_superuser', 'is_active')

    ordering = (
        'email',
    )

    search_fields = ('first_name', 'last_name', 'email')


admin.site.register(User, UserAdmin)
