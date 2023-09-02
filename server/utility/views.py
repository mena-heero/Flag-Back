from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

import pycountry

from .serializers import *
from .models import *


class SettingsApiViewset(viewsets.GenericViewSet):
    @action(
        detail=False,
        methods=["get"],
        permission_classes=(AllowAny,),
    )
    def all(self, request):
        try:
            global_settings_obj = GlobalSetting.objects.first()
            global_settings = GlobalSettingsSerializer(
                global_settings_obj).data
        except:
            global_settings = None

        try:
            social_obj = SocialMediaSettings.objects.first()
            social_settings = SocialMediaSettingsSerializer(social_obj).data
        except:
            social_settings = None

        mainmenu_qs = MainMenu.objects.filter(is_active=True)
        mainmenu = MainMenuSerializer(mainmenu_qs, many=True).data

        footermenu_qs = FooterMenu.objects.filter(is_active=True)
        footermenu = FooterMenuSerializer(footermenu_qs, many=True).data

        return Response(
            {
                "settings": global_settings,
                "social": social_settings,
                "mainmenu": mainmenu,
                "footermenu": footermenu,
            },
            status=status.HTTP_200_OK,
        )


class StoryApiViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Story.objects.all()
    serializer_class = StorySerializer


class AllCountryApiViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = None


class ContactUsApiViewset(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    pagination_class = None
