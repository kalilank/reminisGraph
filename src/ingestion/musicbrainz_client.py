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
    headers=self.headers,
    timeout=30
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
        headers=self.headers,
        timeout=30
    )

    time.sleep(1)
    return response.json()
  
  def get_artist_recordings(self, artist_id, limit=25):
    url = f"{self.BASE_URL}/recording"

    params = {
        "artist": artist_id,
        "fmt": "json",
        "limit": limit
    }

    response = requests.get(
        url,
        params=params,
        headers=self.headers,
        timeout=30
    )

    time.sleep(1)
    response.raise_for_status()
    return response.json()
  
  def get_releases_from_group(self, release_group_id):
    url = f"{self.BASE_URL}/release"
    params = {
        "release-group": release_group_id,
        "fmt": "json"
    }
    response = requests.get(url, params=params, headers=self.headers, timeout=30)
    time.sleep(1)
    response.raise_for_status()
    return response.json()

  def get_release(self, release_id, inc=None):
    url = f"{self.BASE_URL}/release/{release_id}"

    params = {
      "fmt": "json"
    }

    if inc:
      params["inc"] = inc

    response = requests.get(
      url,
      params=params,
      headers=self.headers,
      timeout=30
    )

    time.sleep(1)
    response.raise_for_status()
    return response.json()