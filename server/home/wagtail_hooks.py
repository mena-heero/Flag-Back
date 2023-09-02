from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from instance_selector.registry import registry
from instance_selector.selectors import ModelAdminInstanceSelector
from .models import *


class AuthorAdmin(ModelAdmin):
    model = Author
    menu_icon = "folder"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)
    search_fields = ("name",)


# class CategoryAdmin(ModelAdmin):
#     model = Category
#     menu_icon = "folder"
#     menu_order = 300
#     add_to_settings_menu = False
#     exclude_from_explorer = False
#     list_display = ("name", "slug")
#     search_fields = ("name",)


modeladmin_register(AuthorAdmin)
# modeladmin_register(CategoryAdmin)


class CompanyFinderRatingAdmin(ModelAdmin):
    model = CompanyFinderRating
    menu_icon = "folder"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "rating")
    search_fields = ("title",)


modeladmin_register(CompanyFinderRatingAdmin)
