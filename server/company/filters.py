from django.db.models import Q

from django_filters import rest_framework as filters
from django.contrib.postgres.search import SearchVector
from rest_framework import filters as rest_filter

from .models import *


class CompanyFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    sort_by_name = filters.NumberFilter(method="filter_by_sort_by_name")
    sort_by_rating = filters.NumberFilter(method="filter_by_sort_by_rating")

    def filter_by_sort_by_name(self, queryset, name, value):
        if value is None:
            return queryset

        if int(value) == 0:  # ascending order
            return queryset.order_by("name")
        elif int(value) == 1:  # descending order
            return queryset.order_by("-name")
        else:
            return queryset

    def filter_by_sort_by_rating(self, queryset, name, value):
        if value is None:
            return queryset

        if int(value) == 0:  # ascending order
            return queryset.order_by("-rating")
        elif int(value) == 1:  # descending order
            return queryset.order_by("rating")
        else:
            return queryset

    class Meta:
        model = Company
        fields = [
            "name",
        ]


class RatingFilter(filters.FilterSet):
    class Meta:
        model = RatingReview
        fields = ["type", "news", "articles", "company"]


class SavedTopicFilter(filters.FilterSet):
    class Meta:
        model = SavedTopic
        fields = ["type", ]
