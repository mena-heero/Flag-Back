from .utils import post_on_social
from utility.fields import *


IMAGE_RENDITION_RULES = {"original": "original|jpegquality-60|format-webp"}


def article_post_save(sender, **kwargs):
    instance = kwargs["instance"]
    if instance.post_on_social == True:
        meta_desctiption = instance.search_description
        og_image = instance.og_image
        page_html_url = instance.full_url

        image_url = None
        if og_image:
            image_url = og_image.get_rendition("original|jpegquality-60").full_url

        post_on_social(meta_desctiption, image_url, page_html_url)

        instance.post_on_social = False
        instance.save()


def news_post_save(sender, **kwargs):
    instance = kwargs["instance"]
    if instance.post_on_social == True:
        meta_desctiption = instance.search_description
        og_image = instance.og_image
        page_html_url = instance.full_url

        image_url = None
        if og_image:
            image_url = og_image.get_rendition(
                "original|jpegquality-60").full_url

        post_on_social(meta_desctiption, image_url, page_html_url)

        instance.post_on_social = False
        instance.save()

