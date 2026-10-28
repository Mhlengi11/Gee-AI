import os

import requests

api_key = os.environ.get("YOUTUBE_API_KEY")
if not api_key:
    raise SystemExit("Set the YOUTUBE_API_KEY environment variable before running this script.")

url = "https://www.googleapis.com/youtube/v3/search"
params = {
    "part" : "snippet",
    "q" : "PODCAST AND CHILL NETWORK NEW ERA",
    "type" : "video",
    "key" : api_key

}
response = requests.get(url, params=params)
print(response.status_code)
data = response.json()
for item in data['items']:
    print(item['snippet']['title'])