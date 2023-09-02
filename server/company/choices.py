from django.db import models


class RatingReviewChoice(models.IntegerChoices):
    NEWS = 0, "News"
    ARTICLES = 1, "Articles"
    COMPANY = 2, "Company"


class SavedTopicChoice(models.IntegerChoices):
    NEWS = 0, "News"
    ARTICLES = 1, "Articles"
    COMPANY = 2, "Company"
