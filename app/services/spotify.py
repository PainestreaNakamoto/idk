from pydantic import BaseModel
from typing import List
import abc
import base64
import requests

class SpotifyEntity(BaseModel):
    rank: int
    title: str
    artist: str
    image: str
    time: str
    utl: str


class Spotify(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def all(self):
        pass
    
    @abc.abstractmethod
    def form_id(self):
        pass

class SpotifyService(Spotify):
    def __init__(self):
        self.token: str = ""
        self.__client_id: str = "cb4d05e614dd4771914af54ad8a71f48"
        self.__client_secret: str = "a7f197455ad8417782576fe9ce506658"
        self.__client_credential: str = f"{self.__client_id}:{self.__client_secret}"
        self.__client_credential_b64: str = base64.b64encode(self.__client_credential.encode()).decode()
    
    def all(self) -> List[dict]:

        client_id = "cb4d05e614dd4771914af54ad8a71f48"
        client_secret = "a7f197455ad8417782576fe9ce506658"

        # Encode the client ID and client secret as base64
        client_credentials = f"{client_id}:{client_secret}"
        client_credentials_b64 = base64.b64encode(client_credentials.encode()).decode()

        # Set the headers and data for the POST request
        headers = {
            "Authorization": f"Basic {client_credentials_b64}",
        }
        data = {
            "grant_type": "client_credentials",
        }

        # Send the POST request to get the access token
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers=headers,
            data=data,
        )

        # Parse the JSON response and extract the access token
        access_token = response.json()["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        # Set the parameters for the GET request
        params = {
            "country": "TH",
            "type": "playlist",
        }

        # Send the GET request to get the top 100 music lists of Thailand
        response = requests.get(
            "https://api.spotify.com/v1/playlists/37i9dQZEVXbMnz8KIWsvf9",
            headers=headers,
        )

        # Parse the JSON response and extract the playlist IDs
        #playlist_ids = [item["id"] for item in response.json()["playlists"]["items"]]

        # Print the playlist IDs
        top_100_songs = response.json()["tracks"]["items"]
        new_model_data = []

        for y,i in enumerate(top_100_songs):
            time = i["track"]["duration_ms"] 
            seconds=(time/1000)%60
            seconds = int(seconds)
            minutes=(time/(1000*60))%60
            minutes = int(minutes)
            hours=(time/(1000*60*60))%24
            if len(str(seconds)) == 1:
                seconds = f"0{seconds}"

            full_time = f"{minutes}:{seconds}"

            new_model_data.append({
                    "rank": y+1,
                    "name": i["track"]["name"],
                    "artist": i["track"]["artists"][0]["name"],
                    "image": i["track"]["album"]["images"][0]["url"],
                    "time": f"{full_time}",
                    "url": i["track"]["external_urls"]["spotify"]
                    })


        return new_model_data



    def form_id(self) -> dict:
        pass


