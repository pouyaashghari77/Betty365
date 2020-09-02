import requests
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

from Betty.apps.bets.models import Event


class BWin:
    def __init__(self, *args, **kwargs):
        self.headers = {
            'x-rapidapi-host': "bwin-odds.p.rapidapi.com",
            'x-rapidapi-key': settings.RAPIDAPI_BWIN_API_KEY
        }
        self.urls = {
            'Upcoming Events': 'https://bwin-odds.p.rapidapi.com/v1/bwin/prematch',
            'Live Events': 'https://bwin-odds.p.rapidapi.com/v1/bwin/inplay',
            'Event Result': 'https://bwin-odds.p.rapidapi.com/v1/bwin/result'
        }
        self.supported_sports = {
            'Football': 4,
            'Basketball': 7,
            'Tennis': 5
        }

    def preMatchResults(self, sport_id: int = None):
        params = {"sport_id": sport_id}
        return self._get_bwin_response(params, url=self.urls['Upcoming Events'])

    def inplayResults(self, sport_id: int = None):
        params = {"sport_id": sport_id}
        return self._get_bwin_response(params, url=self.urls['Live Events'])

    def eventResult(self, event_id):
        params = {"event_id": event_id}
        return self._get_bwin_response(params, url=self.urls['Event Result'])

    def _get_bwin_response(self, params, url):
        response_ = requests.request("GET", url, headers=self.headers, params=params)
        return response_.json()['results']

    def updateUpcomingEvents(self):
        result = [self.preMatchResults(sport_id) for sport_id in self.supported_sports.values()]
        result = [item for sublist in result for item in sublist]
        for element in result:
            if not element['HomeTeam']:
                continue
            self._updateOrCreateEvent(element)

    def updateLiveEvents(self):
        self._concludeLiveEvents()

        result = [self.inplayResults(sport_id) for sport_id in self.supported_sports.values()]
        result = [item for sublist in result for item in sublist]
        for element in result:
            if not element['HomeTeam']:
                continue
            self._updateOrCreateEvent(element, match_result=Event.RESULT_LIVE)

    def _concludeLiveEvents(self):
        Event.objects.filter(
            match_result=Event.RESULT_LIVE
        ).update(
            match_result=Event.RESULT_CONCLUDED
        )

    def setConcludedEventsResult(self):
        concluded_events = Event.objects.filter(
            match_result=Event.RESULT_CONCLUDED,
            date__lt=timezone.now(),
        )

        for event in concluded_events:
            scores = self.eventResult(event.external_id)[0].get('ss')
            event.set_result(scores)

    def _updateOrCreateEvent(self, element, match_result=Event.RESULT_UPCOMING):
        event_title = '%s - %s' % (element['HomeTeam'], element['AwayTeam'])
        obj, _ = Event.objects.update_or_create(
            title=event_title,
            slug=slugify(event_title),
            defaults={
                'title': event_title,
                'slug': slugify(event_title),
                'sport_name': element['SportName'],
                'home': element['HomeTeam'],
                'away': element['AwayTeam'],
                'league': element['LeagueName'],
                'region': element['RegionName'],
                'market_results': element['Markets'][0]['results'] if element['Markets'] else '',
                'date': element['Date'],
                'external_id': element['Id'],
                'match_result': match_result
            },
        )
