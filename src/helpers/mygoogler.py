# django_googler -> google.oauth2
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from django.conf import settings


def get_user_creds(user):
    try:
        got = user.google_oauth_token
    except Exception as e:
        raise Exception(f"Google API not active for this user: {e}")
    data = {
        "token": got.access_token,
        "refresh_token": got.refresh_token,
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
        "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
    }
    return Credentials(**data)


def build_service(creds, service_name="people", version="v1"):
    return build(service_name, version, credentials=creds)


def get_my_contacts(user, page_token=None):
    creds = get_user_creds(user)
    service = build_service(creds, service_name="people", version="v1")
    results = (
        service.people()
        .connections()
        .list(
            pageSize=10,
            resourceName="people/me",
            personFields="name,emailAddresses",
            requestSyncToken=True,
            pageToken=page_token,
        )
        .execute()
    )
    return results


def get_my_other_contacts(user, page_token=None):
    creds = get_user_creds(user)
    service = build_service(creds, service_name="people", version="v1")
    results = (
        service.people()
        .otherContacts()
        .list(
            pageSize=10,
            readMask="name,emailAddresses",
            requestSyncToken=True,
            pageToken=page_token,
        )
        .execute()
    )
    return results
