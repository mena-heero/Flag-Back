from django.views import View
from django.shortcuts import redirect, render
from .utils import evest as evest_utils
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django_filters import rest_framework as filters

import pycountry

from .serializers import *
from .models import *
from .filters import *
from .utils.utils import get_country_code_from_ip, get_client_ip, create_analytics


class CreativeApiViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = CreativeSerializer
    queryset = Creative.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CreativeFilter

    @action(
        detail=False,
        methods=["get"],
        permission_classes=(AllowAny,),
        serializer_class=CreativeSerializer,
    )
    def get_creative(self, request):
        brand = request.GET.get("brand")
        name = request.GET.get("creative_name")
        try:
            creative = Creative.objects.get(name=name, brand__slug=brand)
        except:
            creative = None

        if creative:
            data = self.serializer_class(creative).data
            return Response(data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class BrandApiViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class CreativeRedirectView(View):
    template_name = "affiliate/index.html"

    def get(self, request):
        print("Visit Api call")

        query_params = request.GET
        ci = query_params.get("ci")
        uai = query_params.get("uai")

        if not ci or not uai:
            variables = {}
            return render(request, self.template_name, variables)

        user_ip = get_client_ip(request)
        country_code = get_country_code_from_ip(user_ip)

        creative, user, redirect_url, analytics_obj = create_analytics(user_ip, ci, uai)

        if analytics_obj:
            analytics_obj.visitor_country = country_code
            analytics_obj.save()

        if creative == None or user == None:
            variables = {}
            return render(request, self.template_name, variables)

        if redirect_url:
            print("redirect_url", redirect_url)
            return redirect(redirect_url)

        variables = {}
        print("Visit Api success")

        return render(request, self.template_name, variables)


class EvestApiViewset(viewsets.GenericViewSet):
    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=EvestRegistrationSerializer,
    )
    def signup(self, request):
        """
        {
            "firstName": "",
            "lastName": "",
            "email": "",
            "phone": "",
            "countryCode": ""
        }
        """
        data = request.data
        print('Signing up', data)
        ci = data.get("ci", None)
        uai = data.pop("uai", None)
        ani = data.pop("ani", None)
        user_ip = data.pop("user_ip", None)
        analytics_obj = None

        country_code = get_country_code_from_ip(user_ip)

        if uai and ani:
            try:
                analytics_obj = Analytics.objects.get(id=ani)

                if analytics_obj.is_registered:
                    creative, r_user, red_url, analytics_obj = create_analytics(
                        user_ip, ci, uai
                    )
                    if analytics_obj:
                        analytics_obj.visitor_country = country_code
                        analytics_obj.save()
                else:
                    # user checking of analytics table
                    # user = User.objects.get(affiliate_id=uai)
                    # if analytics_obj.user != user:
                    #     analytics_obj.user = user
                    analytics_obj.visitor_ip = user_ip
                    analytics_obj.visitor_country = country_code
                    analytics_obj.save()
            except:
                analytics_obj = None
        elif uai:
            creative, r_user, red_url, analytics_obj = create_analytics(
                user_ip, ci, uai
            )
            if analytics_obj:
                analytics_obj.visitor_country = country_code
                analytics_obj.save()

        serializer = self.serializer_class(
            data=data,
            context={
                "analytics_obj": analytics_obj,
                "country_code": country_code,
                "user_ip": user_ip,
            },
        )

        if serializer.is_valid():
            login_url = serializer.signup()

            return Response({"login_url": login_url}, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

