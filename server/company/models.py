from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
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
from wagtail.search import index
from modelcluster.fields import ParentalKey

from django_extensions.db.fields import AutoSlugField

from .choices import *


# @register_snippet
class Company(models.Model):
    name = models.CharField(_("Company name"), max_length=150)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )
    background_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )
    account_open_link = models.URLField(
        _("Account open link"), max_length=250, null=True, blank=True
    )
    is_islamic = models.BooleanField(_("Is islamic account?"), default=False)
    rating = models.FloatField(_("Rating"), default=0)
    slug = AutoSlugField(
        populate_from=[
            "name",
        ]
    )
    creation_time = models.DateTimeField(_("Creation time"), auto_now_add=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("logo"),
                FieldPanel("background_image"),
                FieldPanel("rating"),
                FieldPanel("is_islamic"),
                FieldPanel("account_open_link"),
            ],
            heading="Basic",
        )
    ]
    search_fields = [
        index.SearchField("name", partial_match=True),
    ]

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ("-creation_time",)


class RatingReview(models.Model):
    user = models.ForeignKey(
        "authentication.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="ratings",
        null=True,
        blank=True,
    )
    type = models.IntegerField(
        _("Rating on"),
        choices=RatingReviewChoice.choices,
        default=RatingReviewChoice.NEWS,
    )
    news = models.ForeignKey(
        "home.NewsDetailPage",
        verbose_name=_("News"),
        on_delete=models.CASCADE,
        related_name="ratings",
        null=True,
        blank=True,
    )
    articles = models.ForeignKey(
        "home.ArticleDetailPage",
        verbose_name=_("Articles"),
        on_delete=models.CASCADE,
        related_name="ratings",
        null=True,
        blank=True,
    )
    company = models.ForeignKey(
        "home.CompanyDetail",
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
        related_name="ratings",
        null=True,
        blank=True,
    )
    rating = models.FloatField(_("Rating"), default=1)
    comment = models.TextField(_("Comment"), null=True, blank=True)
    is_published = models.BooleanField(_("Is published?"), default=False)
    creation_time = models.DateTimeField(_("Creation time"), auto_now_add=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("user"),
                FieldPanel("news"),
                FieldPanel("articles"),
                FieldPanel("company"),
                FieldPanel("rating"),
                FieldPanel("comment"),
            ],
            heading="Basic",
        ),
        MultiFieldPanel(
            [
                FieldPanel("is_published")
            ],
            heading="Accept or Reject",
        )
    ]

    class Meta:
        ordering = ("-creation_time",)


class SavedTopic(models.Model):
    user = models.ForeignKey(
        "authentication.User",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="saved_topics",
        null=True,
        blank=True,
    )
    type = models.IntegerField(
        _("Saved type"),
        choices=SavedTopicChoice.choices,
        default=SavedTopicChoice.ARTICLES,
    )
    news = models.ForeignKey(
        "home.NewsDetailPage",
        verbose_name=_("News"),
        on_delete=models.CASCADE,
        related_name="saved_topics",
        null=True,
        blank=True,
    )
    articles = models.ForeignKey(
        "home.ArticleDetailPage",
        verbose_name=_("Articles"),
        on_delete=models.CASCADE,
        related_name="saved_topics",
        null=True,
        blank=True,
    )
    company = models.ForeignKey(
        "home.CompanyDetail",
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
        related_name="saved_topics",
        null=True,
        blank=True,
    )
    creation_time = models.DateTimeField(_("Creation time"), auto_now_add=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("user"),
                FieldPanel("type"),
                FieldPanel("news"),
                FieldPanel("articles"),
                FieldPanel("company"),
            ],
            heading="Basic",
        )
    ]

    class Meta:
        ordering = ("-creation_time",)


@register_snippet
class Stock(models.Model):
    title = models.CharField(_("Stock title"), max_length=150)
    symbol = models.CharField(
        _("Stock symbol from trading view"), max_length=150)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("symbol"),
                FieldPanel("logo"),
            ],
            heading="Basic",
        )
    ]

    def __str__(self):
        return self.symbol
