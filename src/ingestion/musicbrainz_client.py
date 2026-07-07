import requests
import time

class MusicBrainzClient:
  BASE_URL = "https://musicbrainz.org/ws/2"

  def __init__(self):
    self.headers = {
      "User-Agent": "ReminisGraph/1.0 (learning project)"
    }

  def search_artist(self, artist_name):
    url = f"{self.BASE_URL}/artist"

    params = {
    "query": artist_name,
    "fmt": "json"
    }

    print(url)

    response = requests.get(
    url,
    params=params,
    headers=self.headers
    )
    
    time.sleep(1)
    return response.json()

  def get_artist(self, artist_id, inc=None):
    url = f"{self.BASE_URL}/artist/{artist_id}"

    params = {
      "fmt": "json",
      }
    
    if inc:
        params["inc"] = inc

    response = requests.get(
        url,
        params=params,
        headers=self.headers
    )

    time.sleep(1)
    return response.json()


