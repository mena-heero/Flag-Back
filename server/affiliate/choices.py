from django.db import models


class LanguageChoice(models.IntegerChoices):
    ENGLISH = 0, "English"
    ARABIC = 1, "Arabic"


class CreativeTypeChoice(models.IntegerChoices):
    LINK = 0, "Link"
    BANNER = 1, "Banner"


class CreativeSizeChoice(models.IntegerChoices):
    UNAVAILABLE = 0, "Unavailable"
    SIZE_1920_1080 = 1, "1920 x 1080"
    SIZE_1440_780 = 2, "1440 x 780"


class AnalyticStatusChoice(models.IntegerChoices):
    DEFAULT = 0, "Default"
    ANSWER = 1, "Answer"
    NO_ANSWER = 2, "No Answer"
    INTERESTED = 3, "Interested"
    NOT_INTERESTED = 4, "Not Interested"
    WRONG_NUMBER = 5, "Wrong Number"


class BalanceTypeChoice(models.IntegerChoices):
    CREDIT = 0, "Credit"
    DEBIT = 1, "Debit"
