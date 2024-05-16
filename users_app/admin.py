from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users_app.models import Users


class CustomUserAdmin(UserAdmin):
    model = Users
    exclude = ("username",)
    list_display = (
        "email",
        "first_name",
        "last_name",
        "created_at",
        "updated_at",
    )
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
        ("Permissions", {"fields": ("is_superuser",)}),
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
