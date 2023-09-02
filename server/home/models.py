from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    PageChooserPanel,
    InlinePanel,
)
from wagtail.api import APIField
from wagtail.core.fields import StreamField, RichTextField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from modelcluster.models import ClusterableModel
from wagtail.core.models import Orderable
from modelcluster.fields import ParentalKey
from wagtail.signals import page_published

from django_extensions.db.fields import AutoSlugField

from utility.fields import ImageRenditionField
from utility.serializers import CountrySerializer
from .utils import prepare_richtext_for_api
from . import blocks
from .signals import *


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = AutoSlugField(populate_from="name", editable=True)

    panels = [FieldPanel("name"), FieldPanel("slug")]

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("slug"),
            ],
            heading="Basic",
        )
    ]

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


@register_snippet
class Author(models.Model):
    name = models.CharField(_("Name"), max_length=150)
    desc = models.TextField(_("Desc"), null=True, blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [FieldPanel("name"), FieldPanel("desc"), FieldPanel("image")],
            heading="Basic",
        )
    ]

    def __str__(self):
        return self.name


class BasePage(Page):
    og_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    og_keywords = models.CharField(
        _("Og keywords"), max_length=550, null=True, blank=True
    )

    promote_panels = Page.promote_panels + [
        FieldPanel("og_image", help_text="size: width-1200px, height-630px"),
        FieldPanel("og_keywords"),
    ]

    api_fields = [
        APIField(
            "og_img_original",
            serializer=ImageRenditionField(
                {
                    "original": "original",
                },
                source="og_image",
            ),
        ),
        APIField("og_keywords"),
    ]

    class Meta:
        abstract = True


class HomePage(BasePage):
    title_en = models.CharField(max_length=250, null=True, blank=True)
    body = StreamField(
        [
            ("broker_survey_block", blocks.BrokerSurveyBlock()),
            ("companies", blocks.CompanyBlock()),
            ("news", blocks.HomeNewsBlock()),
            ("articles", blocks.HomeArticleBlock()),
            ("two_column_text_image_block", blocks.HomeTwoColumnTextImageBlock()),
            ("currency_rate_block", blocks.CurrencyRateBlock())
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("title_en"),
        MultiFieldPanel(
            [FieldPanel("body")],
            heading="Body",
        ),
    ]

    api_fields = BasePage.api_fields + [
        APIField("title"),
        APIField("title_en"),
        APIField("body"),
    ]

    parent_page_types = []
    subpage_types = ["home.RedirectPage", "home.BasicPage",]


class BasicPage(BasePage):
    title_en = models.CharField(max_length=250, null=True, blank=True)
    body = StreamField(
        [
            ("description", blocks.DescriptionBlock()),
            ("image_block", blocks.ImageBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("title_en"),
        MultiFieldPanel(
            [FieldPanel("body")],
            heading="Body",
        ),
    ]

    api_fields = BasePage.api_fields + [
        APIField("title"),
        APIField("title_en"),
        APIField("body"),
    ]

    parent_page_types = [
        "home.HomePage",
        "home.RedirectPage",
    ]
    subpage_types = []


class RedirectPage(Page):
    title_en = models.CharField(max_length=250, null=True, blank=True)

    hero_title = models.CharField(
        _("Hero title"), max_length=250, null=True, blank=True
    )
    hero_title_en = models.CharField(
        _("Hero title en"), max_length=250, null=True, blank=True
    )
    hero_description = RichTextField(
        _("Hero description"), null=True, blank=True)
    hero_description_en = RichTextField(
        _("Hero description en"), null=True, blank=True)
    list_title = models.CharField(
        _("List title"), max_length=250, null=True, blank=True
    )
    list_title_en = models.CharField(
        _("List title en"), max_length=250, null=True, blank=True
    )
    og_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    og_keywords = models.CharField(
        _("Og keywords"), max_length=550, null=True, blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("title_en"),
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_title_en"),
                FieldPanel("hero_description"),
                FieldPanel("hero_description_en"),
                FieldPanel("list_title"),
                FieldPanel("list_title_en"),
            ],
            heading="Header data",
        )
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("og_image"),
        FieldPanel("og_keywords"),
    ]

    @property
    def all_categories(self):
        if self.slug in ["news", "articles"]:
            from .serializers import RedirectPageSerializer

            childs = self.get_children()
            return RedirectPageSerializer(childs, many=True).data
        return None

    @property
    def rendered_hero_description(self):
        return prepare_richtext_for_api(self.hero_description)

    @property
    def rendered_hero_description_en(self):
        # return prepare_richtext_for_api(self.hero_description_en)
        return self.hero_description_en

    api_fields = [
        APIField("title"),
        APIField("title_en"),
        APIField(
            "og_img_original",
            serializer=ImageRenditionField(
                {
                    "original": "original",
                },
                source="og_image",
            ),
        ),
        APIField("og_keywords"),
        APIField("hero_title"),
        APIField("hero_title_en"),
        APIField("rendered_hero_description"),
        APIField("rendered_hero_description_en"),
        APIField("list_title"),
        APIField("list_title_en"),
        APIField("all_categories"),
    ]

    parent_page_types = ["home.HomePage", "home.RedirectPage"]
    subpage_types = [
        "home.RedirectPage",
        "home.NewsDetailPage",
        "home.ArticleDetailPage",
        "home.BasicPage",
        "home.CompanyDetail",
        "home.ContactUsPage",
        "home.PrivatePage"
    ]


class PrivatePage(BasePage):
    from .serializers import AuthorSerializer

    title_en = models.CharField(max_length=250, null=True, blank=True)

    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(
        [
            ("description", blocks.DescriptionBlock()),
            ("button_block", blocks.ButtonBlock()),
            ("image_block", blocks.ImageBlock()),
            ("banner", blocks.BannerBlock()),
            ("table_block", blocks.TableBlock()),
            ("custom_table_block", blocks.CustomTableBlock()),
            ("video_block", blocks.VideoBlock())
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    author = models.ForeignKey(
        "Author",
        verbose_name=_("Author"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    reading_time = models.CharField(
        _("Reading time"), max_length=250, null=True, blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("title_en"),
        MultiFieldPanel(
            [
                FieldPanel("thumbnail", help_text="252x372 pixel"),
                FieldPanel("reading_time"),
            ],
            heading="Header",
        ),
        MultiFieldPanel(
            [
                FieldPanel("author"),
            ],
            heading="Author",
        ),
        MultiFieldPanel([FieldPanel("body")], heading="Body"),
    ]

    api_fields = BasePage.api_fields + [
        APIField("title"),
        APIField("title_en"),
        APIField("reading_time"),
        APIField(
            "thumbnail",
            serializer=ImageRenditionField(
                {"original": "original|format-webp"}),
        ),
        APIField("author", serializer=AuthorSerializer()),
        APIField("body"),
    ]

    parent_page_types = [
        "home.RedirectPage",
    ]
    subpage_types = []


class ContactUsPage(BasePage):
    title_en = models.CharField(max_length=250, null=True, blank=True)

    hero_title = models.CharField(
        _("Hero title"), max_length=250, null=True, blank=True
    )
    hero_title_en = models.CharField(
        _("Hero title en"), max_length=250, null=True, blank=True
    )
    hero_subtitle = models.CharField(
        _("Hero subtitle"), max_length=250, null=True, blank=True
    )
    hero_subtitle_en = models.CharField(
        _("Hero subtitle en"), max_length=250, null=True, blank=True
    )

    background_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    background_image_en = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("title_en"),
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_title_en"),
                FieldPanel("hero_subtitle"),
                FieldPanel("hero_subtitle_en"),
                FieldPanel("background_image", help_text="252x372 pixel"),
                FieldPanel("background_image_en", help_text="252x372 pixel"),
            ],
            heading="Basic",
        )
    ]

    api_fields = BasePage.api_fields + [
        APIField("title"),
        APIField("title_en"),
        APIField("hero_title"),
        APIField("hero_title_en"),
        APIField("hero_subtitle"),
        APIField("hero_subtitle_en"),
        APIField(
            "background_image",
            serializer=ImageRenditionField(
                {"original": "original|format-webp"}),
        ),
        APIField(
            "background_image_en",
            serializer=ImageRenditionField(
                {"original": "original|format-webp"}),
        ),
    ]

    parent_page_types = ["home.HomePage", "home.RedirectPage"]
    subpage_types = []


class NewsDetailPage(BasePage):
    from .serializers import AuthorSerializer

    title_en = models.CharField(max_length=250, null=True, blank=True)

    post_on_social = models.BooleanField(_("Post on social?"), default=False)
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    thumbnail_en = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(
        [
            ("description", blocks.DescriptionBlock()),
            ("button_block", blocks.ButtonBlock()),
            ("image_block", blocks.ImageBlock()),
            ("banner", blocks.BannerBlock()),
            ("table_block", blocks.TableBlock()),
            ("custom_table_block", blocks.CustomTableBlock()),
            ("video_block", blocks.VideoBlock())
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    author = models.ForeignKey(
        "Author",
        verbose_name=_("Author"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    reading_time = models.CharField(
        _("Reading time"), max_length=250, null=True, blank=True
    )

    @property
    def fetch_parent(self):
        obj = self.get_parent()
        return {
            "id": obj.specific.id,
            "title": obj.specific.title,
            "title_en": obj.specific.title_en,
            "slug": obj.specific.slug,
        }

    content_panels = Page.content_panels + [
        FieldPanel("title_en"),
        MultiFieldPanel(
            [
                FieldPanel("thumbnail", help_text="252x372 pixel"),
                FieldPanel("thumbnail_en", help_text="252x372 pixel"),
                FieldPanel("reading_time"),
            ],
            heading="Header",
        ),
        MultiFieldPanel(
            [
                FieldPanel("post_on_social"),
            ],
            heading="Social Post",
        ),
        MultiFieldPanel(
            [
                FieldPanel("author"),
            ],
            heading="Author",
        ),
        MultiFieldPanel([FieldPanel("body")], heading="Body"),
    ]

    api_fields = BasePage.api_fields + [
        APIField("title"),
        APIField("title_en"),
        APIField("reading_time"),
        APIField(
            "thumbnail",
            serializer=ImageRenditionField(
                {"original": "original|jpegquality-80|format-webp"}),
        ),
        APIField(
            "thumbnail_en",
            serializer=ImageRenditionField(
                {"original": "original|jpegquality-80|format-webp"}),
        ),
        APIField("author", serializer=AuthorSerializer()),
        APIField("body"),
        APIField("fetch_parent"),
    ]

    parent_page_types = [
        "home.RedirectPage",
    ]
    subpage_types = []


class ArticleDetailPage(BasePage):
    from .serializers import AuthorSerializer

    title_en = models.CharField(max_length=250, null=True, blank=True)

    post_on_social = models.BooleanField(_("Post on social?"), default=False)
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    thumbnail_en = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(
        [
            ("description", blocks.DescriptionBlock()),
            ("button_block", blocks.ButtonBlock()),
            ("image_block", blocks.ImageBlock()),
            ("banner", blocks.BannerBlock()),
            ("table_block", blocks.TableBlock()),
            ("custom_table_block", blocks.CustomTableBlock()),
            ("video_block", blocks.VideoBlock())
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    author = models.ForeignKey(
        "Author",
        verbose_name=_("Author"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    reading_time = models.CharField(
        _("Reading time"), max_length=250, null=True, blank=True
    )

    @property
    def fetch_parent(self):
        obj = self.get_parent()
        return {
            "id": obj.specific.id,
            "title": obj.specific.title,
            "title_en": obj.specific.title_en,
            "slug": obj.specific.slug,
        }

    content_panels = Page.content_panels + [
        FieldPanel("title_en"),
        MultiFieldPanel(
            [
                FieldPanel("thumbnail", help_text="252x372 pixel"),
                FieldPanel("thumbnail_en", help_text="252x372 pixel"),
                FieldPanel("reading_time"),
            ],
            heading="Header",
        ),
        MultiFieldPanel(
            [
                FieldPanel("post_on_social"),
            ],
            heading="Social Post",
        ),
        MultiFieldPanel(
            [
                FieldPanel("author"),
            ],
            heading="Author",
        ),
        MultiFieldPanel([FieldPanel("body")], heading="Body"),
    ]

    api_fields = BasePage.api_fields + [
        APIField("title"),
        APIField("title_en"),
        APIField("reading_time"),
        APIField(
            "thumbnail",
            serializer=ImageRenditionField(
                {"original": "original|jpegquality-80|format-webp"}),
        ),
        APIField(
            "thumbnail_en",
            serializer=ImageRenditionField(
                {"original": "original|jpegquality-80|format-webp"}),
        ),
        APIField("author", serializer=AuthorSerializer()),
        APIField("body"),
        APIField("fetch_parent"),
    ]

    parent_page_types = [
        "home.RedirectPage",
    ]
    subpage_types = []


class CompanyDetail(BasePage):
    title_en = models.CharField(max_length=250, null=True, blank=True)

    short_description = models.TextField(
        _("Short description"), null=True, blank=True)
    short_description_en = models.TextField(
        _("Short description en"), null=True, blank=True)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )
    thumbnail_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )
    thumbnail_image_en = models.ForeignKey(
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
    regulatory_body = models.CharField(
        _("Regulatory bodies"), max_length=250, null=True, blank=True)
    minimum_deposit = models.IntegerField(_("Minimum deposit"), default=0)
    origin_branch = models.ForeignKey("utility.Country", verbose_name=_(
        "Main branch"), on_delete=models.SET_NULL, null=True, blank=True, related_name="companies")
    customer_service = models.CharField(
        _("Customer service"), max_length=150, null=True, blank=True)
    demo_account = models.BooleanField(_("Demo account?"), default=True)
    trading_platforms = models.CharField(
        _("Trading platforms"), max_length=250, null=True, blank=True)
    markets_products = models.CharField(
        _("Market and products"), max_length=250, null=True, blank=True)

    overal_evaluation = models.FloatField(_("Overal evaluation"), default=0)
    fees_rating = models.FloatField(_("Fees rating"), default=0)
    regulation_rating = models.FloatField(_("Regulation rating"), default=0)
    deposit_withdraw_rating = models.FloatField(
        _("Deposit and withdraw ratings"), default=0)
    commissions_rating = models.FloatField(_("Commissions rating"), default=0)
    assets_rating = models.FloatField(_("Assets rating"), default=0)
    trading_platform_rating = models.FloatField(
        _("Trading platform ratings"), default=0)
    research_development_rating = models.FloatField(
        _("Research and development rating"), default=0)
    customer_service_rating = models.FloatField(
        _("Customer service rating"), default=0)
    mobile_app_trading_rating = models.FloatField(
        _("Mobile app trading rating"), default=0)
    learning_rating = models.FloatField(_("Learning rating"), default=0)
    experience_with_broker_rating = models.FloatField(
        _("Experience with broker rating"), default=0)
    trading_tools_rating = models.FloatField(
        _("Trading tools rating"), default=0)
    website_rating = models.FloatField(_("Website rating"), default=0)
    security_rating = models.FloatField(_("Security rating"), default=0)
    leverage = models.CharField(
        _("Leverage"), max_length=50, null=True, blank=True)

    recommendation_text = models.TextField(
        _("Recommendation text"), null=True, blank=True)
    recommendation_text_en = models.TextField(
        _("Recommendation text en"), null=True, blank=True)

    body = StreamField(
        [
            ("description", blocks.DescriptionBlock()),
            ("button_block", blocks.ButtonBlock()),
            ("image_block", blocks.ImageBlock()),
            ("banner", blocks.BannerBlock()),
            ("table_block", blocks.TableBlock()),
            ("custom_table_block", blocks.CustomTableBlock()),
            ("company_evaluation_block", blocks.CompanyEvaluationBlock()),
            ("video_block", blocks.VideoBlock())
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    company_slug = AutoSlugField(
        populate_from=[
            "title",
        ]
    )
    creation_time = models.DateTimeField(_("Creation time"), auto_now_add=True)

    content_panels = Page.content_panels + [
        FieldPanel("title_en"),
        MultiFieldPanel(
            [
                FieldPanel("short_description"),
                FieldPanel("short_description_en"),
                FieldPanel("logo", help_text="65x65 pixel"),
                FieldPanel("thumbnail_image", help_text="192x166 pixel"),
                FieldPanel("thumbnail_image_en", help_text="192x166 pixel"),
                FieldPanel("rating"),
                FieldPanel("is_islamic"),
                FieldPanel("account_open_link"),
                FieldPanel("regulatory_body"),
                FieldPanel("minimum_deposit"),
                FieldPanel("origin_branch"),
                FieldPanel("customer_service"),
                FieldPanel("demo_account"),
                FieldPanel("trading_platforms"),
                FieldPanel("markets_products"),
                FieldPanel("leverage"),
                FieldPanel("recommendation_text"),
                FieldPanel("recommendation_text_en")
            ],
            heading="Basic",
        ),
        MultiFieldPanel(
            [
                FieldPanel("overal_evaluation"),
                FieldPanel("fees_rating"),
                FieldPanel("regulation_rating"),
                FieldPanel("deposit_withdraw_rating"),
                FieldPanel("commissions_rating"),
                FieldPanel("assets_rating"),
                FieldPanel("trading_platform_rating"),
                FieldPanel("research_development_rating"),
                FieldPanel("customer_service_rating"),
                FieldPanel("mobile_app_trading_rating"),
                FieldPanel("learning_rating"),
                FieldPanel("experience_with_broker_rating"),
                FieldPanel("trading_tools_rating"),
                FieldPanel("website_rating"),
                FieldPanel("security_rating")
            ],
            heading="Evaluation",
        ),
        MultiFieldPanel(
            [
                FieldPanel("body"),
            ],
            heading="Evaluation",
        )
    ]

    api_fields = BasePage.api_fields + [
        APIField("title"),
        APIField("title_en"),
        APIField("short_description"),
        APIField("short_description_en"),
        APIField(
            "logo",
            serializer=ImageRenditionField(
                {
                    "original": "original|jpegquality-80|format-webp",
                },
            ),
        ),
        APIField(
            "thumbnail_image",
            serializer=ImageRenditionField(
                {
                    "original": "original|jpegquality-80|format-webp",
                },
            ),
        ),
        APIField(
            "thumbnail_image_en",
            serializer=ImageRenditionField(
                {
                    "original": "original|jpegquality-80|format-webp",
                },
            ),
        ),
        APIField("rating"),
        APIField("is_islamic"),
        APIField("account_open_link"),
        APIField("regulatory_body"),
        APIField("minimum_deposit"),
        APIField("origin_branch", serializer=CountrySerializer("origin_branch")),
        APIField("customer_service"),
        APIField("demo_account"),
        APIField("trading_platforms"),
        APIField("overal_evaluation"),
        APIField("regulation_rating"),
        APIField("deposit_withdraw_rating"),
        APIField("commissions_rating"),
        APIField("assets_rating"),
        APIField("trading_platform_rating"),
        APIField("research_development_rating"),
        APIField("customer_service_rating"),
        APIField("mobile_app_trading_rating"),
        APIField("learning_rating"),
        APIField("experience_with_broker_rating"),
        APIField("trading_tools_rating"),
        APIField("website_rating"),
        APIField("company_slug"),
        APIField("body")
    ]

    parent_page_types = [
        "home.RedirectPage",
    ]
    subpage_types = []


class CompanyChooser(Orderable):
    page = ParentalKey("CompanyFinderRating", related_name="companies")
    company = models.ForeignKey(
        "home.CompanyDetail", verbose_name=_("Company"), on_delete=models.CASCADE)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("company"),
            ],
            heading="Basic",
        ),
    ]


class CompanyFinderRating(ClusterableModel):
    title = models.CharField(blank=True, null=True, max_length=150)
    title_en = models.CharField(blank=True, null=True, max_length=150)
    rating = models.CharField(blank=True, null=True, max_length=150)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("title_en"),
                FieldPanel("rating"),
            ],
            heading="Basic",
        ),
        InlinePanel("companies", label="Company"),
    ]


# ─── Signals ──────────────────────────────────────────────────────────────────

page_published.connect(article_post_save, sender=ArticleDetailPage)
page_published.connect(news_post_save, sender=NewsDetailPage)
