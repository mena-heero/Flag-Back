from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from django_filters import rest_framework as filters

from .serializers import *
from .models import *
from .filters import *
from .permissions import *


class CompanyApiViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Company.objects.all()
    serializer_class = HomeCompanySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CompanyFilter


class RatingReviewApiViewset(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    queryset = RatingReview.objects.filter(is_published=True)
    serializer_class = RatingReviewSerializer
    # permission_classes = (IsAuthenticatedOrReadOnlyPermission,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RatingFilter

    def get_serializer_context(self):
        d = super().get_serializer_context()
        if self.request.user.is_authenticated:
            d["user"] = self.request.user
        else:
            d["user"] = None
        return d


class SavedTopicApiViewset(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin
):
    """
    {
        "type": 1,
        "articles": id
    }
    """
    serializer_class = SavedTopicSerializer
    permission_classes = (
        IsAuthenticated, IsAuthenticatedOrReadOnlyPermission,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SavedTopicFilter

    def get_serializer_context(self):
        d = super().get_serializer_context()
        if self.request.user.is_authenticated:
            d["user"] = self.request.user
        else:
            d["user"] = None
        return d

    def get_queryset(self):
        return SavedTopic.objects.filter(user=self.request.user)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=(IsAuthenticated,),
    )
    def is_exists(self, request):
        user = request.user
        obj_id = request.GET.get("obj_id")
        type = request.GET.get("type")
        exists = False

        if not obj_id or not type:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        type = int(type)

        if type == SavedTopicChoice.ARTICLES:
            exists = user.saved_topics.filter(
                type=type, articles=obj_id).exists()
            if exists == True:
                obj = user.saved_topics.get(
                    type=type, articles=obj_id)
                return Response({
                    "exists": True,
                    "id": obj.id})
            else:
                return Response({
                    "exists": False,
                    "id": None
                })

        elif type == SavedTopicChoice.NEWS:
            exists = user.saved_topics.filter(
                type=type, news=obj_id).exists()
        elif type == SavedTopicChoice.COMPANY:
            exists = user.saved_topics.filter(
                type=type, company=obj_id).exists()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
