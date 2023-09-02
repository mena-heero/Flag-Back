from random import randint

from django.apps import apps


def generate_otp(n=6):
    range_start = 10 ** (n - 1)
    range_end = (10**n) - 1
    return randint(range_start, range_end)


def generate_affiliate_id(n=5):
    User = apps.get_model("authentication", "User")

    range_start = 10 ** (n - 1)
    range_end = (10**n) - 1
    aff_id = randint(range_start, range_end)

    while User.objects.filter(affiliate_id=aff_id).exists():
        aff_id = randint(range_start, range_end)
    return aff_id
