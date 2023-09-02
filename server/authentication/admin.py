from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "join_date",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("full_name", "email")


admin.site.register(User, UserAdmin)


class VerificationAdmin(admin.ModelAdmin):
    list_display = ("email", "code")
    search_fields = ("email",)


admin.site.register(Verification, VerificationAdmin)
admin.site.register(SocialAuthData)
