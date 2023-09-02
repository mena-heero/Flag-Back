from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)


from .models import *


class MainMenuAdmin(ModelAdmin):
    model = MainMenu
    menu_icon = "folder"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("link_title", "link_url", "is_active")
    search_fields = ("link_title",)
    list_filter = ("is_active",)
    ordering = ("sort_order",)


class StoryAdmin(ModelAdmin):
    model = Story
    menu_icon = "folder"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "link", "creation_time")
    search_fields = ("title",)


modeladmin_register(StoryAdmin)


class FooterMenuAdmin(ModelAdmin):
    model = FooterMenu
    menu_icon = "folder"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "is_active")
    search_fields = ("title",)
    list_filter = ("is_active",)
    ordering = ("sort_order",)


class MenuGroup(ModelAdminGroup):
    menu_label = "Menus"
    menu_icon = "folder-open-inverse"
    menu_order = 200
    items = (
        MainMenuAdmin,
        FooterMenuAdmin,
    )


modeladmin_register(MenuGroup)


class ContactUsAdmin(ModelAdmin):
    model = ContactUs
    menu_icon = "folder"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("full_name", "email", "phone", "is_replied", "creation_time")
    search_fields = ("full_name", "email", "phone")
    list_filter = ("is_replied",)


modeladmin_register(ContactUsAdmin)
