from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import UserProfileManager
from .utils import *
from .tasks import *
from .choices import *


class User(AbstractBaseUser, PermissionsMixin):
    auth_type = models.IntegerField(
        _("Auth type"), choices=AuthTypeChoice.choices, default=AuthTypeChoice.DEFAULT
    )
    user_type = models.IntegerField(
        _("Auth type"), choices=UserTypeChoice.choices, default=UserTypeChoice.USER
    )
    affiliate_id = models.IntegerField(_("Affiliate ID"), null=True, blank=True)
    full_name = models.CharField(_("Full name"), max_length=100, null=True, blank=True)
    email = models.EmailField(_("Email"), max_length=100, unique=True)
    country = models.ForeignKey(
        "utility.Country",
        verbose_name=_("Country"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    phone = models.CharField(_("Phone number"), max_length=150, null=True, blank=True)
    profile_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    social_image_url = models.URLField(
        _("Social Image url"), max_length=200, null=True, blank=True
    )
    is_email_verified = models.BooleanField(_("Is email verified?"), default=False)

    join_date = models.DateTimeField(
        _("Join date"), auto_now_add=True, null=True, blank=True
    )

    is_active = models.BooleanField(_("Is active"), default=True)
    is_staff = models.BooleanField(_("Is staff"), default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    class Meta:
        ordering = ("-join_date",)

    def send_verification_code(self, email=None, reason=None):
        if email:
            obj, created = Verification.objects.get_or_create(email=email)
            if not created:
                obj.code = generate_otp()
                obj.save()
            otp_email_queue.delay(email, obj.code, reason)


class Verification(models.Model):
    email = models.EmailField(_("Email"), max_length=100)
    code = models.IntegerField(_("Code"), default=generate_otp, null=True, blank=True)

    def __str__(self):
        return str(self.email)


class SocialAuthData(models.Model):
    social_id = models.CharField(_("Social id"), max_length=150)
    data = models.JSONField(_("Data"), null=True, blank=True)
    signup_data = models.JSONField(_("Signup data"), null=True, blank=True)


# ─── Post Save Signal ─────────────────────────────────────────────────────────
@receiver(post_save, sender=User)
def user_post_save(sender, instance, **kwargs):
    if instance.user_type == UserTypeChoice.AFFILIATE:
        if not instance.affiliate_id:
            instance.affiliate_id = generate_affiliate_id()
            instance.save()
