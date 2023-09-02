import requests
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from ..models import *
from authentication.models import User


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_country_code_from_ip(ip):
    # try:
    #     g = GeoIP2()
    #     obj = g.city(ip)
    #     country_code = obj["country_code"]
    # except:
    #     country_code = "BD"
    try:
        api_key = "75fa599932b340ebabd02f4361b217b8"
        endpoint = f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip}"
        x = requests.get(endpoint)
        content = x.json()
        country = content.get("country_code2", None)
        if country == None:
            return "BD"
        return country
    except:
        return "BD"


def create_analytics(ip, ci, uai):
    try:
        creative = Creative.objects.get(id=ci)
    except:
        creative = None

    try:
        user = User.objects.get(affiliate_id=uai)
    except:
        user = None

    if creative == None or user == None:
        return None, None, None, None

    analytics_obj, created = Analytics.objects.get_or_create(
        user=user, creative=creative, visitor_ip=ip, is_registered=False
    )
    analytics_obj.visit_count = analytics_obj.visit_count + 1
    analytics_obj.save()
    template = creative.template
    redirect_url = f"{settings.AFFILIATE_DOMAIN}/{template.brand.slug}/{template.file_name}?ci={ci}&uai={uai}&ani={analytics_obj.id}"
    return creative, user, redirect_url, analytics_obj
