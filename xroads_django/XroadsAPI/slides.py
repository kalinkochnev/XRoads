from typing import Dict, List, Match, Optional
from googleapiclient.discovery import build
from google.auth import load_credentials_from_file, default
from django.conf import settings

import re
PREZ_REGEX = r"^(.*docs\.google\.com\/presentation\/)((d\/e\/)|(d\/))(?P<id>[^\/]*).*"
slide_png_url = lambda prez_id, slide_id: f'https://docs.google.com/presentation/d/{prez_id}/export/png?id={prez_id}&pageid={slide_id}' 

def create_credentials():
    credentials = load_credentials_from_file(settings.GOOGLE_KEY_FILE.name) # TODO fixme!!!
    return build('slides', 'v1', credentials=credentials[0])


def is_valid(url: str) -> Optional[Match[str]]:
    match = re.search(PREZ_REGEX, url)
    return match

def get_slides(url: str):
    service = create_credentials()
    valid = is_valid(url)

    if valid is not None:
        prez_id = valid.group('id')

        response = {}
        try:
            response = service.presentations().get(presentationId=prez_id).execute()
        except:
            response['slides'] = []
            
        return prez_id, response['slides']

    return []

def find_yt_url(slide):
    for element in slide['pageElements']:
        if 'video' in element.keys():
            return element['video']['url']
    return

def get_slide_urls(url: str):
    pres_id, slides = get_slides(url)
    urls = []

    for slide in slides:
        yt_url = find_yt_url(slide)
        if yt_url:
            urls.append(yt_url)
        else:
            urls.append(slide_png_url(pres_id, slide['objectId']))

    return urls

