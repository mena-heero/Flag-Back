import requests

from wagtail.core.models import Site
from wagtail.core.rich_text import expand_db_html

from decouple import config


def prepare_richtext_for_api(value):
    s = Site.objects.get(is_default_site=True)
    current_site = s.root_url
    replace_text = 'src="{0}/'.format(current_site)
    html_data = expand_db_html(value)
    html_data = html_data.replace('src="/', replace_text)
    return html_data


def post_on_social(description=None, image=None, page_link=None):
    if description != None:
        extra_in_description = f"View the full article on: {page_link}"
        modified_desc = f"{description} \n\n\n{extra_in_description}"

        fb_page_access_token = config("FB_PAGE_ACCESS_TOKEN")
        fb_page_id = config("FB_PAGE_ID")

        if image != None:
            fb_endpoint = f"https://graph.facebook.com/{fb_page_id}/photos"
        else:
            fb_endpoint = f"https://graph.facebook.com/{fb_page_id}/feed"

        params = {
            "message": modified_desc,
            "access_token": fb_page_access_token
        }

        if image != None:
            params["url"] = image

        content = requests.post(fb_endpoint, params=params)
        print(content.content)
