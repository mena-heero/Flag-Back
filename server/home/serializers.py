from rest_framework import serializers

from .models import Author, RedirectPage


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class RedirectPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedirectPage
        fields = ("id", "title", "title_en", "slug")
