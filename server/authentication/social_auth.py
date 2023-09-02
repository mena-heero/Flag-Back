import requests
import json

from rest_framework.authtoken.models import Token

from .choices import *
from .models import User, SocialAuthData


def facebook_authenticate(auth_code=""):
    access_token_uri = "https://graph.facebook.com/v4.0/oauth/access_token"
    redirect_uri = "https://flagedu.com/socialauth/facebook"

    params = {
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': "1419617315245410",
        'client_secret': "73f7fd31e14ba971a3004c8b6bce30ae",
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    content = requests.post(
        access_token_uri, data=params, headers=headers)

    content_decode = json.loads(content.content.decode("utf-8"))
    access_token = content_decode["access_token"]

    fields = "id,name,picture"

    user_data = requests.get(
        f"https://graph.facebook.com/me?access_token={access_token}&fields={fields}")

    user_data_decode = json.loads(user_data.content.decode("utf-8"))
    user_id = user_data_decode["id"]
    obj, created = SocialAuthData.objects.get_or_create(social_id=user_id)
    if created:
        obj.data = user_data_decode
        obj.save()
    return user_data_decode


def google_authenticate(auth_code):
    access_token_uri = "https://accounts.google.com/o/oauth2/token"
    redirect_uri = "https://flagedu.com/socialauth/google"

    params = {
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': "559204491251-9rdnbjf2n27ks6u5klvef778icg1j4rm.apps.googleusercontent.com",
        'client_secret': "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",
        'grant_type': 'authorization_code',
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    content = requests.post(
        access_token_uri, data=params, headers=headers)

    content_decode = json.loads(content.content.decode("utf-8"))
    access_token = content_decode["access_token"]

    user_data = requests.get(
        f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}")

    user_data_decode = json.loads(user_data.content.decode("utf-8"))
    return user_data_decode


def validate_social_signup(user_data, auth_type=AuthTypeChoice.GOOGLE):
    # return type: status, auth_type, user
    if auth_type == AuthTypeChoice.GOOGLE:
        email = user_data.get("email", None)
        full_name = user_data.get("name", None)
        profile_image_url = user_data.get("picture", None)

        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            user = User.objects.get(email=email)
            if user.auth_type == AuthTypeChoice.GOOGLE:
                return True, AuthTypeChoice.GOOGLE, user
            else:
                user_auth_type = user.auth_type
                return False, user_auth_type, None
        else:
            user = User.objects.create(
                auth_type=AuthTypeChoice.GOOGLE, email=email, full_name=full_name, is_email_verified=True, social_image_url=profile_image_url)
            return True, AuthTypeChoice.GOOGLE, user
    elif auth_type == AuthTypeChoice.FACEBOOK:
        social_id = user_data.get("id")
        try:
            social_obj = SocialAuthData.objects.get(social_id=social_id)
        except:
            social_obj = None

        if social_obj:
            if social_obj.signup_data:
                signup_data = social_obj.signup_data
                email = signup_data.get("email")
                try:
                    user = User.objects.get(email=email)
                except:
                    user = None
                if user:
                    return True, AuthTypeChoice.FACEBOOK, user
                else:
                    return False, AuthTypeChoice.FACEBOOK, None
            else:
                return False, AuthTypeChoice.FACEBOOK, None
        else:
            return False, AuthTypeChoice.FACEBOOK, None


def generate_token(user):
    token, token_created = Token.objects.get_or_create(user=user)
    return token.key
