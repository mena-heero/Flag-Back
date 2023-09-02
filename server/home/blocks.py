from django.utils.functional import cached_property

from wagtail.coreutils import resolve_model_string
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock as DefaultImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock

from .utils import prepare_richtext_for_api
from company.models import Company, Stock
from company.serializers import HomeCompanySerializer, StockSerializer


class SnippetChooserBlock(blocks.ChooserBlock):
    def __init__(self, target_model, serializer=None, **kwargs):
        super().__init__(**kwargs)
        self._target_model = target_model
        self.serializer = serializer

    def get_api_representation(self, value, context=None):
        if value:
            if self.serializer:
                return self.serializer(value).data
            else:
                return self.get_prep_value(value)

    @cached_property
    def target_model(self):
        if isinstance(self._target_model, str):
            return resolve_model_string(self._target_model)
        return self._target_model

    @cached_property
    def widget(self):
        from wagtail.snippets.widgets import AdminSnippetChooser

        return AdminSnippetChooser(self.target_model)

    class Meta:
        icon = "snippet"


class PageChooserBlock(blocks.PageChooserBlock):
    def to_python(self, value):

        if value is None:
            return value
        else:
            try:
                return (
                    self.target_model.objects.filter(pk=value)
                    .only("id", "title", "slug")
                    .first()
                )
            except self.target_model.DoesNotExist:
                return None

    def bulk_to_python(self, values):
        objects = self.target_model.objects.only(
            "id", "title", "slug").in_bulk(values)
        return [objects.get(id) for id in values]

    def get_api_representation(self, value, context=None):
        if value:
            return {
                "id": value.id,
                "link": value.get_url(context["request"]),
                "title": value.title,
            }


class ImageChooserBlock(DefaultImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            data = {
                "id": value.id,
                "title": value.title,
                "original": value.get_rendition("original|jpegquality-80|format-webp").attrs_dict,
            }
            rules = getattr(self.meta, "rendition_rules", False)
            if rules:
                for name, rule in rules.items():
                    data[name] = value.get_rendition(rule).attrs_dict
            return data


class RichTextBlock(blocks.RichTextBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return prepare_richtext_for_api(value.source)
        else:
            return ""


BROKER_SURVEY_IMAGE_RENDITION_RULES = {
    "original": "original|jpegquality-80|format-webp",
}


class BrokerSurveyBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=250)
    title_en = blocks.CharBlock(max_length=250, required=False)
    subtitle = blocks.CharBlock(max_length=250)
    subtitle_en = blocks.CharBlock(max_length=250, required=False)

    image = ImageChooserBlock(
        rendition_rules=BROKER_SURVEY_IMAGE_RENDITION_RULES)
    image_en = ImageChooserBlock(
        rendition_rules=BROKER_SURVEY_IMAGE_RENDITION_RULES)

    learn_more_button_text = blocks.CharBlock(max_length=250)
    learn_more_button_text_en = blocks.CharBlock(max_length=250, required=False)
    learn_more_button_link = blocks.CharBlock(max_length=250)
    survey_button_text = blocks.CharBlock(max_length=250)
    survey_button_text_en = blocks.CharBlock(max_length=250, required=False)
    survey_button_link = blocks.CharBlock(max_length=250)


class SingleCompanyBlock(blocks.StructBlock):
    company = SnippetChooserBlock(
        target_model=Company, serializer=HomeCompanySerializer
    )


class CompanyListChooserBlock(blocks.PageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            obj = value.specific
            obj_detail = {
                "id": value.id,
                "slug": value.slug,
                "html_url": obj.get_url(),
                "title": value.title,
                "is_islamic": value.is_islamic,
                "rating": value.rating,
                "account_open_link": value.account_open_link,
                "thumbnail_image": obj.thumbnail_image.get_rendition(
                    "original|jpegquality-80|format-webp"
                ).attrs_dict,
            }
            if obj.thumbnail_image_en is not None:
                obj_detail["thumbnail_image_en"] = obj.thumbnail_image_en.get_rendition("original|jpegquality-80|format-webp").attrs_dict
            else:
                obj_detail["thumbnail_image_en"] = None
            return obj_detail


class CompanyBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=250)
    title_en = blocks.CharBlock(max_length=250, required=False)
    # companies = blocks.ListBlock(SingleCompanyBlock())
    company = blocks.ListBlock(
        CompanyListChooserBlock(page_type="home.CompanyDetail"))


class DescriptionBlock(blocks.StructBlock):
    desc = RichTextBlock()
    desc_en = RichTextBlock(required=False)


class PageOrLinkBlock(blocks.StreamBlock):
    page = PageChooserBlock(max_num=1)
    link = blocks.URLBlock(max_num=1)

    class Meta:
        max_num = 1
        icon = "link"

    def get_api_representation(self, value, context=None):
        try:
            val = value[0]
            if val.block_type == "page":
                page_type = val.value.specific.specific_class.__name__

                if page_type in ["NewsDetailPage", "ArticleDetailPage"]:
                    link = val.value.specific.get_url()
                else:
                    link = val.value.get_url(context["request"])
                    link = link[:-1]
            else:
                link = val.value
            return {"type": val.block_type, "link": link}
        except Exception:
            return {"type": None, "link": None}


class ButtonBlock(blocks.StructBlock):
    link = PageOrLinkBlock()
    label = blocks.CharBlock()
    label_en = blocks.CharBlock(required=False)

    class Meta:
        icon = "link"


IMAGE_BLOCK_RENDITION_RULES = {
    "original": "original|jpegquality-80|format-webp",
}


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(rendition_rules=IMAGE_BLOCK_RENDITION_RULES)
    image_en = ImageChooserBlock(rendition_rules=IMAGE_BLOCK_RENDITION_RULES)


class BannerBlock(blocks.StructBlock):
    image = ImageChooserBlock(rendition_rules=IMAGE_BLOCK_RENDITION_RULES)
    image_en = ImageChooserBlock(rendition_rules=IMAGE_BLOCK_RENDITION_RULES)
    link = PageOrLinkBlock()


class NewsDetailPageChooserBlock(blocks.PageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            obj = value.specific
            obj_detail = {
                "id": value.id,
                "slug": value.slug,
                "html_url": obj.get_url(),
                "title": value.title,
                "thumbnail": obj.thumbnail.get_rendition(
                    "original|jpegquality-80|format-webp"
                ).attrs_dict,
                "publish_date": obj.first_published_at,
            }
            if obj.thumbnail_en is not None:
                obj_detail["thumbnail_en"] = obj.thumbnail_en.get_rendition("original|jpegquality-80|format-webp").attrs_dict
            else:
                obj_detail["thumbnail_en"] = None
            return obj_detail

class HomeNewsBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=250)
    title_en = blocks.CharBlock(max_length=250, required=False)
    news = blocks.ListBlock(NewsDetailPageChooserBlock(
        page_type="home.NewsDetailPage"))


class ArticleDetailPageChooserBlock(blocks.PageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            obj = value.specific
            obj_detail = {
                "id": value.id,
                "slug": value.slug,
                "html_url": obj.get_url(),
                "title": value.title,
                "thumbnail": obj.thumbnail.get_rendition(
                    "original|jpegquality-80|format-webp"
                ).attrs_dict,
                "publish_date": obj.first_published_at,
            }
            if obj.thumbnail_en is not None:
                obj_detail["thumbnail_en"] = obj.thumbnail_en.get_rendition("original|jpegquality-80|format-webp").attrs_dict
            else:
                obj_detail["thumbnail_en"] = None
            return obj_detail


class HomeArticleBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=250)
    title_en = blocks.CharBlock(max_length=250, required=False)
    articles = blocks.ListBlock(
        ArticleDetailPageChooserBlock(page_type="home.ArticleDetailPage")
    )


class HomeTwoColumnTextImageBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=250)
    title_en = blocks.CharBlock(max_length=250, required=False)
    description = RichTextBlock()
    description_en = RichTextBlock(required=False)
    link = ButtonBlock()
    image = ImageChooserBlock(rendition_rules=IMAGE_BLOCK_RENDITION_RULES)
    image_en = ImageChooserBlock(rendition_rules=IMAGE_BLOCK_RENDITION_RULES)


class CustomTableBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=250)
    title_en = blocks.CharBlock(max_length=250, required=False)
    table = TableBlock()
    table_en = TableBlock()


class CompanyEvaluationBlock(blocks.StaticBlock):
    class Meta:
        label = "Company evaluation"


class VideoBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=250, required=False)
    title_en = blocks.CharBlock(max_length=250, required=False)
    youtube_video_id = blocks.CharBlock(max_length=250)


class StockBlock(blocks.StructBlock):
    stock = SnippetChooserBlock(
        target_model=Stock, serializer=StockSerializer
    )


class CurrencyTab(blocks.StructBlock):
    title = blocks.CharBlock(max_length=250, required=False)
    title_en = blocks.CharBlock(max_length=250, required=False)
    stocks = blocks.ListBlock(StockBlock())


class CurrencyRateBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=250, required=False)
    title_en = blocks.CharBlock(max_length=250, required=False)
    tabs = blocks.ListBlock(CurrencyTab())
