from typing import List, Match, Optional
from googleapiclient.discovery import build
from google.auth import load_credentials_from_file, default
from django.conf import settings

import re

PREZ_REGEX = r"^.*docs\.google\.com\/presentation\/d\/(?P<id>[^\/]*).*"
slide_svg_url = lambda prez_id, slide_id: f'https://docs.google.com/presentation/d/{prez_id}/export/svg?id={prez_id}&pageid={slide_id}' 

def create_credentials():
    credentials = load_credentials_from_file(settings.GOOGLE_KEY_FILE.name) # TODO fixme!!!
    return build('slides', 'v1', credentials=credentials[0])


def is_valid(url: str) -> Optional[Match[str]]:
    match = re.search(PREZ_REGEX, url)
    return match

def get_slides(url: str) -> List[str]:
    service = create_credentials()
    valid = is_valid(url)

    if valid is not None:
        prez_id = valid.group('id')
        response = service.presentations().get(presentationId=prez_id).execute()
        slide_ids = [slide['objectId'] for slide in response['slides']]
        return [slide_svg_url(prez_id, slide_id) for slide_id in slide_ids]
    return []
