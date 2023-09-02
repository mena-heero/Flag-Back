from django.db import models


class AuthTypeChoice(models.IntegerChoices):
    DEFAULT = 0, "Default"
    GOOGLE = 1, "Google"
    FACEBOOK = 2, "Facebook"


class UserTypeChoice(models.IntegerChoices):
    USER = 0, "User"
    AFFILIATE = 1, "Affiliate"
