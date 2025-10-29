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
            pageSize=2,
            resourceName="people/me",
            personFields="names,emailAddresses",
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
        service.otherContacts()
        .list(
            pageSize=2,
            readMask="names,emailAddresses",
            requestSyncToken=True,
            pageToken=page_token,
        )
        .execute()
    )
    return results


def parse_contact_info(data):
    contacts = []
    contact_list = data.get("otherContacts") or data.get("connections")
    if not contact_list:
        return contacts
    for contact in contact_list:
        contact_info = {
            "email": None,
            "first_name": None,
            "last_name": None,
        }
        email_addresses = contact.get("emailAddresses", [])
        for email_data in email_addresses:
            if email_data.get("metadata", {}).get("primary", False):
                contact_info["email"] = email_data.get("value")
                break
        if not contact_info["email"] and email_addresses:
            contact_info["email"] = email_addresses[0].get("value")
        names = contact.get("names", [])
        if names:
            primary_name = None
            for name_data in names:
                if name_data.get("metadata", {}).get("primary", False):
                    primary_name = name_data
                    break
            if not primary_name:
                primary_name = names[0]
            contact_info["first_name"] = primary_name.get("givenName")
            contact_info["last_name"] = primary_name.get("familyName")
            # contact_info['full_name'] = primary_name.get('displayName')
        contacts.append(contact_info)
    return contacts
