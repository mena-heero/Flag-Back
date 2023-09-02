from django.db.models import Q

from django_filters import rest_framework as filters
from django.contrib.postgres.search import SearchVector
from rest_framework import filters as rest_filter

from .models import *


class CreativeFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    brand = filters.CharFilter(method="filter_by_brand")
    sort_by_time = filters.CharFilter(method="filter_sort_by_time")

    def filter_sort_by_time(self, queryset, name, value):
        if value is None:
            return queryset

        if int(value) == 0:  # ascending order
            return queryset.order_by("-creation_time")
        elif int(value) == 1:  # descending order
            return queryset.order_by("creation_time")
        else:
            return queryset

    def filter_by_brand(self, queryset, name, value):
        if value is None:
            return queryset

        return queryset.filter(brand__name__icontains=value)

    class Meta:
        model = Creative
        fields = [
            "name",
            "language",
            "type",
            "size",
            "brand",
        ]
