from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from django_filters import rest_framework as filters

from .page_serializer import *
from .models import *
from .filters import *


class CompanyDetailApiViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = CompanyDetailForFindBrokerSerializer
    queryset = CompanyDetail.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CompanyFilter

    def get_serializer_class(self):
        if self.action == "list":
            return CompanyDetailForFindBrokerSerializer
        elif self.action == "retrieve":
            return CompanyDetailForComparisonSerializer

    def list(self, request, *args, **kwargs):
        obj = super().list(request, *args, **kwargs)
        obj_dict = obj.__dict__
        result = obj.__dict__["data"]["results"][:5]
        obj_dict["data"]["results"] = result
        return Response(obj_dict["data"], status=status.HTTP_200_OK)


class CompanyFinderRatingApiViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = CmpanyFinderRatingSerializer
    queryset = CompanyFinderRating.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = CompanyFinderRating.objects.all()
        data = self.serializer_class(queryset, many=True).data

        return Response(data, status=status.HTTP_200_OK)
