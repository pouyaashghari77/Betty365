import requests
from django.conf import settings


class BWin:
    def __init__(self, *args, **kwargs):
        self.headers = {
            'x-rapidapi-host': "bwin-odds.p.rapidapi.com",
            'x-rapidapi-key': settings.RAPIDAPI_BWIN_API_KEY
        }

    def eventDetail(self, event_id):
        payload = '{}'
        params = {"event_id": event_id}
        url_ = "https://bwin-odds.p.rapidapi.com/v1/bwin/event"
        response_ = requests.request("GET", url_, data=payload, headers=self.headers, params=params)
        return response_.text

    def preMatchResults(self, event_id: str = ""):
        url_ = "https://bwin-odds.p.rapidapi.com/v1/bwin/prematch"
        params = {"event_id": event_id}
        response_ = requests.request("GET", url_, headers=self.headers, params=params)
        return response_.json()['results']

    def inplayResults(self, sport_id: str = ""):
        url_ = "https://bwin-odds.p.rapidapi.com/v1/bwin/inplay"
        params = {"sport_id": sport_id}
        response_ = requests.request("GET", url_, headers=self.headers, params=params)
        return response_.json()['results']
