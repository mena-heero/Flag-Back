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
from wagtail.search import index

from django_extensions.db.fields import AutoSlugField

from .choices import *


@register_snippet
class Brand(index.Indexed, models.Model):
    name = models.CharField(_("Name"), max_length=150)
    slug = AutoSlugField(
        populate_from=[
            "name",
        ]
    )

    search_fields = [
        index.SearchField("name", boost=10),
        index.AutocompleteField("name", boost=10),
        index.SearchField("slug"),
    ]

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
            ],
            heading="Basic",
        )
    ]

    def __str__(self):
        return self.name


@register_snippet
class Template(index.Indexed, models.Model):
    brand = models.ForeignKey(
        "affiliate.Brand", verbose_name=_("Brand"), on_delete=models.CASCADE
    )
    name = models.CharField(_("Template name"), max_length=150)
    preview_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    file_name = models.CharField(_("File name"), max_length=150)
    creation_time = models.DateTimeField(
        _("Creation time"), auto_now_add=True, null=True
    )

    search_fields = [
        index.SearchField("name", boost=10),
        index.AutocompleteField("name", boost=10),
    ]

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("brand"),
                FieldPanel("name"),
                FieldPanel("preview_image"),
                FieldPanel("file_name"),
            ],
            heading="Basic",
        )
    ]

    def __str__(self):
        return self.name


class Creative(models.Model):
    brand = models.ForeignKey(
        "affiliate.Brand", verbose_name=_("Brand"), on_delete=models.CASCADE
    )
    template = models.ForeignKey(
        "affiliate.Template",
        verbose_name=_("Tempalate"),
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.CharField(_("Name"), max_length=150)
    language = models.IntegerField(
        _("Language"), choices=LanguageChoice.choices, default=LanguageChoice.ENGLISH
    )
    type = models.IntegerField(
        _("Creative type"),
        choices=CreativeTypeChoice.choices,
        default=CreativeTypeChoice.LINK,
    )
    size = models.IntegerField(
        _("Creative size"),
        choices=CreativeSizeChoice.choices,
        default=CreativeSizeChoice.UNAVAILABLE,
    )
    creation_time = models.DateTimeField(_("Creation time"), auto_now_add=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("brand"),
                FieldPanel("template"),
                FieldPanel("name"),
                FieldPanel("language"),
                FieldPanel("type"),
                FieldPanel("size"),
            ],
            heading="Basic",
        )
    ]

    class Meta:
        ordering = ("-creation_time",)

    def __str__(self):
        return f"{self.brand.name} - {self.name}"


class Analytics(models.Model):
    user = models.ForeignKey(
        "authentication.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="analytics",
    )
    creative = models.ForeignKey(
        "affiliate.Creative",
        verbose_name=_("Creative"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analytics",
    )
    country = models.ForeignKey(
        "utility.Country",
        verbose_name=_("Country"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analytics",
    )
    user_identification = models.CharField(
        _("User id"), max_length=50, null=True, blank=True
    )
    registration_date = models.DateTimeField(
        _("Registration date"), null=True, blank=True
    )
    afp = models.CharField(_("AFP"), max_length=150, null=True, blank=True)
    status = models.IntegerField(
        _("User status"),
        choices=AnalyticStatusChoice.choices,
        default=AnalyticStatusChoice.DEFAULT,
    )
    qftd = models.IntegerField(_("QFTD"), default=0)
    qualification_date = models.DateTimeField(
        _("Qualification date"), null=True, blank=True
    )
    position_count = models.IntegerField(_("Position count"), default=0)
    first_deposit = models.FloatField(_("First Deposit"), default=0)
    first_deposit_date = models.DateTimeField(
        _("First deposit date"), null=True, blank=True
    )
    net_deposits = models.FloatField(_("Net Deposit"), default=0)
    deposit_count = models.IntegerField(_("Deposit count"), default=0)
    account_id = models.CharField(_("Account ID"), max_length=50, null=True, blank=True)
    customer_name = models.CharField(
        _("Customer name"), max_length=150, null=True, blank=True
    )
    commission = models.FloatField(_("Commission"), default=0)
    visitor_country = models.CharField(
        _("Visitor country"), max_length=150, null=True, blank=True
    )
    visitor_ip = models.GenericIPAddressField(
        _("IP address"), protocol="both", unpack_ipv4=False, null=True, blank=True
    )
    visit_count = models.IntegerField(_("Visit Count"), default=0)
    is_registered = models.BooleanField(_("Is Registered?"), default=False)
    creation_time = models.DateTimeField(_("Creation time"), auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Balance(models.Model):
    user = models.ForeignKey(
        "authentication.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="balance",
    )
    analytics = models.ForeignKey(
        "affiliate.Analytics",
        verbose_name=_("Analytics"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    type = models.IntegerField(
        _("Balance type"),
        choices=BalanceTypeChoice.choices,
        default=BalanceTypeChoice.CREDIT,
    )
    amount = models.FloatField(_("Amount"), default=0)

    def __str__(self):
        return str(self.user)


class PaymentDetail(models.Model):
    user = models.ForeignKey(
        "authentication.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="payment_detail",
    )
    vat_id = models.CharField(_("100"), max_length=150, null=True, blank=True)
    account_beneficiary = models.CharField(
        _("Account beneficiary"), max_length=150, null=True, blank=True
    )
    account_number = models.CharField(_("Account number"), max_length=50)
    bank_name = models.CharField(_("Bank name"), max_length=100)
    bank_branch = models.CharField(_("Bank branch"), max_length=100)
    bank_country = models.ForeignKey(
        "utility.Country",
        verbose_name=_("Country"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    bank_city = models.CharField(_("Bank city"), max_length=100)
    swift_code = models.CharField(_("Swift code"), max_length=50)
    iban_number = models.CharField(
        _("IBAN Number"), max_length=50, null=True, blank=True
    )

    def __str__(self):
        return str(self.user)
