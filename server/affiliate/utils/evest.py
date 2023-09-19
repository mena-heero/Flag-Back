import requests
import hashlib
import json
import time
from decouple import config


def make_sha1(s, encoding="utf-8"):
    return hashlib.sha1(s.encode(encoding)).hexdigest()


def create_access_key(time):
    PARTNER_ID = config("partner_id")
    PARTNER_SECRET_KEY = config("partner_secret_key")

    TIME = time
    concatenated_string = PARTNER_ID + str(TIME) + PARTNER_SECRET_KEY
    ACCESS_KEY = make_sha1(concatenated_string)
    return ACCESS_KEY


def get_evest_token():
    url = "https://mena-evest.pandats-api.io/api/v3/authorization"

    l_time = int(time.time())
    access_key = create_access_key(l_time)
    print("access_key: " + access_key)
    partner_id = config("partner_id"),

    data = {
        "partnerId": partner_id,
        "time": str(l_time),
        "accessKey": access_key,
    }

    data_json = json.dumps(data)

    headers = {
        "Content-Type": "application/json",
    }

    r = requests.post(url, headers=headers, data=data_json)
    json_data = r.json()

    try:
        token = json_data["data"]["token"]
        print("Evest Token created successfully: " + str(token))
    except:
        token = None
    return token


def create_customer(data):
    token = get_evest_token()
    url = "https://mena-evest.pandats-api.io/api/v3/customers"
    authorization = "Bearer %s" % token
    headers = {"Content-Type": "application/json", "Authorization": authorization}

    data = {
        "email": data.get("email"),
        "country": data.get("country_code"),
        "firstName": data.get("firstName"),
        "lastName": data.get("lastName"),
        "phone": data.get("phone"),
        "ip": data.get("user_ip"),
        "password": "nstu1234",
        "referral": "partner_id=c1a486dd6c8f128d0be36f669aa221fe|referal_id=35075_398162_EF02|affiliate_id=35075|Aff_id=35075|src=https://economyflow.com",
        "acceptPromotions": True,
        "acceptTermsAndConditions": True,
    }

    data_json = json.dumps(data)
    print("creating customer...!")
    r = requests.post(url, headers=headers, data=data_json)
    content = r.json()

    print("Evest Customer Created Successfully ---> ", content)

    login_data = {
        "email": data['email'],
    }

    data_json = json.dumps(login_data)

    headers = {"Content-Type": "application/json", "Authorization": authorization}
    login_url = "https://mena-evest.pandats-api.io/api/v3/system/loginToken"

    r = requests.post(login_url, headers=headers, data=data_json)
    json_data = r.json()

    print("Evest Customer login Successfully ---> ", json_data)
    return json_data['data']['url']
