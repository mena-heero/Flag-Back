from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)


from .models import *


class LeadAdmin(ModelAdmin):
    model = Lead
    menu_icon = "folder"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("email", "name", "message")
    search_fields = ("name", "email",)
  


modeladmin_register(LeadAdmin)