from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)


from .models import *


class BrandAdmin(ModelAdmin):
    model = Brand
    menu_icon = "folder"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "slug")
    search_fields = ("name", "slug")


class TemplateAdmin(ModelAdmin):
    model = Template
    menu_icon = "folder"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "brand", "creation_time")
    search_fields = ("name", "brand__name", "brand__slug")


class CreativeAdmin(ModelAdmin):
    model = Creative
    menu_icon = "folder"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "brand", "language", "type")
    search_fields = ("name", "brand__name", "brand__slug",)
    list_filter = ("language", "type")


class CreativeGroup(ModelAdminGroup):
    menu_label = "Creatives"
    menu_icon = "folder-open-inverse"
    menu_order = 100
    items = (
        BrandAdmin,
        TemplateAdmin,
        CreativeAdmin,
    )


modeladmin_register(CreativeGroup)
