import os
from datetime import date
import requests
from dotenv import load_dotenv

load_dotenv()

HUBSPOT_BASE = "https://api.hubapi.com"

MOCK_CONTACTS = [
    {
        "persona": "head_of_agency",
        "firstname": "Rachel",
        "lastname": "Monroe",
        "email": "rachel.monroe@agencymock.io",
    },
    {
        "persona": "creative",
        "firstname": "Jordan",
        "lastname": "Voss",
        "email": "jordan.voss@agencymock.io",
    },
    {
        "persona": "pm",
        "firstname": "Marcus",
        "lastname": "Chen",
        "email": "marcus.chen@agencymock.io",
    },
]


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {os.environ['HUBSPOT_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    }


def _create_contact(contact: dict) -> str:
    payload = {
        "properties": {
            "firstname": contact["firstname"],
            "lastname": contact["lastname"],
            "email": contact["email"],
            "hs_persona": contact["persona"],
        }
    }
    resp = requests.post(
        f"{HUBSPOT_BASE}/crm/v3/objects/contacts",
        headers=_headers(),
        json=payload,
    )
    if resp.status_code == 409:
        existing = requests.get(
            f"{HUBSPOT_BASE}/crm/v3/objects/contacts/{contact['email']}",
            headers=_headers(),
            params={"idProperty": "email"},
        )
        existing.raise_for_status()
        return existing.json()["id"]
    resp.raise_for_status()
    return resp.json()["id"]


def _create_note(contact_id: str, blog_title: str, newsletter: str) -> str:
    note_body = (
        f"Blog Title: {blog_title}\n"
        f"Send Date: {date.today().isoformat()}\n\n"
        f"Newsletter Content:\n{newsletter}"
    )
    payload = {
        "properties": {
            "hs_note_body": note_body,
            "hs_timestamp": f"{date.today().isoformat()}T00:00:00Z",
        },
        "associations": [
            {
                "to": {"id": contact_id},
                "types": [
                    {
                        "associationCategory": "HUBSPOT_DEFINED",
                        "associationTypeId": 202,
                    }
                ],
            }
        ],
    }
    resp = requests.post(
        f"{HUBSPOT_BASE}/crm/v3/objects/notes",
        headers=_headers(),
        json=payload,
    )
    resp.raise_for_status()
    return resp.json()["id"]


def distribute_to_hubspot(
    blog_title: str,
    newsletter_head: str,
    newsletter_creative: str,
    newsletter_pm: str,
) -> str:
    newsletters = {
        "head_of_agency": newsletter_head,
        "creative": newsletter_creative,
        "pm": newsletter_pm,
    }

    summary_lines = []

    for contact in MOCK_CONTACTS:
        contact_id = _create_contact(contact)
        newsletter = newsletters[contact["persona"]]
        note_id = _create_note(contact_id, blog_title, newsletter)

        summary_lines.append(
            f"[{contact['persona']}] {contact['firstname']} {contact['lastname']} "
            f"<{contact['email']}> → contact_id={contact_id}, note_id={note_id}"
        )

    return "HubSpot Distribution Summary:\n" + "\n".join(summary_lines)
