from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users_app.models import Users


class CustomUserAdmin(UserAdmin):
    model = Users
    list_display = ("email", "first_name", "last_name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        ("Permissions", {"fields": ("is_admin",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(Users, CustomUserAdmin)
