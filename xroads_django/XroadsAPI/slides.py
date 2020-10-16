from googleapiclient.discovery import build
from google.auth import load_credentials_from_file
import re

presentation_url = "https://docs.google.com/presentation/d/15CG2Iore-8OsyhTlYGB0RR4Bu2FqDbgmpo_UlVBTe9E/edit?usp=sharing"
url_regex = r"^.*docs\.google\.com\/presentation\/d\/(?P<id>[^\/]*).*"

matches = re.search(url_regex, presentation_url)
pres_id = matches.group('id')

credentials = load_credentials_from_file('api_keys.json')
service = build('slides', 'v1', credentials=credentials[0])

result = service.presentations().get(presentationId=pres_id).execute()

slide_ids = [slide['objectId'] for slide in result['slides']]

svg_links = []
for slide_id in slide_ids:
    link = f'https://docs.google.com/presentation/d/{pres_id}/export/svg?id={pres_id}&pageid={slide_id}'
    svg_links.append(link)

