from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import StreamField, RichTextField
from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    PageChooserPanel,
    InlinePanel,
)
from wagtail.snippets.models import register_snippet
from modelcluster.models import ClusterableModel
from wagtail.core.models import Orderable
from modelcluster.fields import ParentalKey

from django_extensions.db.fields import AutoSlugField


@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(
        max_length=255, null=True, blank=True, help_text="Facebook URL"
    )
    linkedin = models.URLField(
        max_length=255, null=True, blank=True, help_text="Linkedin URL"
    )
    instagram = models.URLField(
        max_length=255, null=True, blank=True, help_text="Instagram URL"
    )
    youtube = models.URLField(
        max_length=255, null=True, blank=True, help_text="Youtube URL"
    )
    tiktok = models.URLField(
        max_length=255, null=True, blank=True, help_text="Tiktok URL"
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("facebook"),
                FieldPanel("linkedin"),
                FieldPanel("instagram"),
                FieldPanel("youtube"),
                FieldPanel("tiktok"),
            ],
        )
    ]


@register_setting
class GlobalSetting(BaseSetting):
    company_logo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )
    company_logo_large = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )
    contact_email = models.EmailField(_("Contact email"), max_length=254, null=True, blank=True)
    contact_number = models.CharField(
        _("Contact number"), max_length=30, null=True, blank=True
    )
    address = models.TextField(
        _("Address"), max_length=500, blank=True, null=True)
    address_en = models.TextField(
        _("Address en"), max_length=500, blank=True, null=True)
    copyright_text = models.CharField(
        _("Copyright Text"), max_length=350, blank=True, null=True
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("company_logo"),
                FieldPanel("company_logo_large"),
                FieldPanel("contact_email"),
                FieldPanel("contact_number"),
                FieldPanel("address"),
                FieldPanel("address_en"),
                FieldPanel("copyright_text"),
            ],
            heading="Basic",
        )
    ]


class ContactUs(models.Model):
    full_name = models.CharField(_("Full name"), max_length=150, null=True, blank=True)
    email = models.EmailField(
        _("Email"), max_length=250)
    phone = models.CharField(
        _("Phone"), max_length=50, null=True, blank=True)
    message = models.TextField(
        _("Message"), null=True, blank=True)
    is_replied = models.BooleanField(_("Is replied?"), default=False)
    creation_time = models.DateTimeField(_("Creation time"), auto_now_add=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("full_name"),
                FieldPanel("email"),
                FieldPanel("phone"),
                FieldPanel("message"),
            ],
            heading="Basic",
        )
    ]

    def __str__(self):
        return self.email


#
# ────────────────────────────────────────────────── I ──────────
#   :::::: M E N U S : :  :   :    :     :        :          :
# ────────────────────────────────────────────────────────────
#


class MainMenuItem(Orderable):
    link_title = models.CharField(blank=True, null=True, max_length=50)
    link_title_en = models.CharField(blank=True, null=True, max_length=50)
    link_url = models.CharField(max_length=500, null=True, blank=True)
    companies = models.ForeignKey("home.CompanyDetail", verbose_name=_(
        "Company"), on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    page = ParentalKey("MainMenu", related_name="sub_nav_items")

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("link_title"),
                FieldPanel("link_title_en"),
                FieldPanel("link_url"),
                PageChooserPanel("companies"),
                FieldPanel("is_active"),
            ],
            heading="Menu Item",
        ),
    ]

    def __str__(self):
        return self.link_title

    @property
    def get_link(self):
        if self.companies:
            return self.companies.get_url()
        return self.link_url

    @property
    def get_is_external(self):
        if self.companies:
            return False
        return True


class MainMenu(ClusterableModel):
    link_title = models.CharField(blank=True, null=True, max_length=50)
    link_title_en = models.CharField(blank=True, null=True, max_length=50)
    link_url = models.CharField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.SmallIntegerField(_("Sort order"), default=0)

    class Meta:
        ordering = ("sort_order",)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("link_title"),
                FieldPanel("link_title_en"),
                FieldPanel("link_url"),
                FieldPanel("is_active"),
            ],
            heading="Menu Item",
        ),
        MultiFieldPanel(
            [
                FieldPanel("sort_order"),
            ],
            heading="Sorting",
        ),
        InlinePanel("sub_nav_items", label="SubMenu Item"),
    ]

    def __str__(self):
        return self.link_title

    @property
    def get_is_external(self):
        if self.link_url:
            check = self.link_url[0:5]
            if check == "https":
                return True
            return False
        return False


class FooterMenuItem(Orderable):
    link_title = models.CharField(blank=True, null=True, max_length=50)
    link_title_en = models.CharField(blank=True, null=True, max_length=50)
    link_url = models.CharField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    page = ParentalKey("FooterMenu", related_name="footer_nav_items")

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("link_title"),
                FieldPanel("link_title_en"),
                FieldPanel("link_url"),
                FieldPanel("is_active"),
            ],
            heading="Menu Item",
        ),
    ]

    def __str__(self):
        return self.link_title

    @property
    def get_is_external(self):
        if self.link_url:
            check = self.link_url[0:5]
            if check == "https":
                return True
            return False
        return False


class FooterMenu(ClusterableModel):
    title = models.CharField(blank=True, null=True, max_length=150)
    title_en = models.CharField(blank=True, null=True, max_length=150)
    is_active = models.BooleanField(default=True)
    sort_order = models.SmallIntegerField(_("Sort order"), default=0)

    class Meta:
        ordering = ("sort_order",)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("title_en"),
                FieldPanel("is_active"),
            ],
            heading="Menu Item",
        ),
        MultiFieldPanel(
            [
                FieldPanel("sort_order"),
            ],
            heading="Sorting",
        ),
        InlinePanel("footer_nav_items", label="SubMenu Item"),
    ]


class Story(models.Model):
    title = models.CharField(_("Title"), max_length=250)
    title_en = models.CharField(_("Title en"), null=True, blank=True, max_length=250)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )
    image_en = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )
    link = models.CharField(_("Link"), max_length=250, null=True, blank=True)
    creation_time = models.DateTimeField(_("Creation time"), auto_now_add=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("title_en"),
                FieldPanel(
                    "image", help_text="120x120 pixel"),
                FieldPanel(
                    "image_en", help_text="120x120 pixel"),
                FieldPanel("link"),
            ],
            heading="Basic",
        ),
    ]

    def __str__(self):
        return self.title

    @property
    def get_is_external(self):
        if self.link:
            check = self.link[0:5]
            if check == "https":
                return True
            return False
        return False


@register_snippet
class Country(models.Model):
    alpha_2 = models.CharField(_("Alpha 2"), max_length=2)
    alpha_3 = models.CharField(_("Alpha 3"), max_length=3)
    name = models.CharField(_("Name"), max_length=100)
    official_name = models.CharField(
        _("Official name"), max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name
