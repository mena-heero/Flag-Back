from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register


from .models import *


# class CompanyAdmin(ModelAdmin):
#     model = Company
#     menu_icon = "folder"
#     menu_order = 300
#     add_to_settings_menu = False
#     exclude_from_explorer = False
#     list_display = ("name", "rating", "slug", "creation_time")
#     search_fields = ("name", "slug")


# modeladmin_register(CompanyAdmin)


class StockAdmin(ModelAdmin):
    model = Stock
    menu_icon = "folder"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "symbol",)
    search_fields = ("title", "symbol")


modeladmin_register(StockAdmin)


class RatingReviewAdmin(ModelAdmin):
    model = RatingReview
    menu_icon = "folder"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("user", "rating", "is_published", "creation_time")
    search_fields = ("user__email", "user__full_name")
    list_filter = ("is_published",)


modeladmin_register(RatingReviewAdmin)
