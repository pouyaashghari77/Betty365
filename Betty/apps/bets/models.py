from django.db import models


class Event(models.Model):
    RESULT_UPCOMING = 'Upcoming'
    RESULT_LIVE = 'Live'
    RESULT_CONCLUDED = 'Concluded'
    RESULT_HOME_WIN = 'Home Win'
    RESULT_AWAY_WIN = 'Away Win'
    RESULT_DRAW = 'Draw'
    RESULT_CANCELLED = 'Cancelled'
    RESULT_CHOICES = (
        (RESULT_UPCOMING, 'Upcoming'),
        (RESULT_LIVE, 'Live'),
        (RESULT_CONCLUDED, 'Concluded'),
        (RESULT_HOME_WIN, 'Home Win'),
        (RESULT_AWAY_WIN, 'Away Win'),
        (RESULT_DRAW, 'Draw'),
        (RESULT_CANCELLED, 'Cancelled'),
    )

    title = models.CharField('Title', max_length=64)
    slug = models.SlugField('Slug', max_length=64)

    sport_name = models.CharField(max_length=64, blank=True, null=True)
    league = models.CharField(max_length=64, blank=True, null=True)
    region = models.CharField(max_length=64, blank=True, null=True)

    home = models.CharField('Home', max_length=64)
    away = models.CharField('Away', max_length=64)
    # home_odds = models.FloatField('Home Odds')
    # away_odds = models.FloatField('Away Odds')
    # draw_odds = models.FloatField('Draw Odds')
    scores = models.CharField('Scores', max_length=64, blank=True, null=True)
    date = models.DateTimeField('Date')
    match_result = models.CharField('Match Result', max_length=32,
                                    choices=RESULT_CHOICES, default=RESULT_UPCOMING,
                                    blank=True, null=True)
    market_results = models.TextField('Market Results', default='', blank=True, null=True)
    external_id = models.CharField('External API ID', max_length=64, default='')
    created = models.DateTimeField('Created at', auto_now_add=True)
    updated = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f'{self.home} - {self.away}'

    def set_result(self, scores=None):
        if scores is None:
            return

        self.scores = scores
        scores = [s.split('-') for s in scores.split(',')]
        scores = [[int(float(j)) for j in i] for i in scores]
        scores = [sum(i) for i in zip(*scores)]
        try:
            if scores[0] > scores[1]:
                self.match_result = self.RESULT_HOME_WIN
            elif scores[1] > scores[0]:
                self.match_result = self.RESULT_AWAY_WIN
            else:
                self.match_result = self.RESULT_DRAW
        except IndexError:
            pass

        self.full_clean()
        self.save()


class Bet(models.Model):
    SIDE_BACK = 'Back'
    SIDE_LAY = 'Lay'
    SIDE_CHOICES = (
        (SIDE_BACK, 'Back'),
        (SIDE_LAY, 'Lay'),
    )
    event = models.ForeignKey('Event', models.CASCADE, verbose_name='Event')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,
                             related_name='bets', verbose_name='User')
    selection = models.CharField('Selection', max_length=64)
    side = models.CharField('Side', max_length=4)
    odds = models.FloatField('Odds')
    stake = models.FloatField('Stake')
    matched = models.BooleanField('Matched', default=False)
    matched_with = models.ForeignKey('self', blank=True, null=True, related_name='matched_bets',
                                     on_delete=models.SET_NULL, verbose_name='Matched With')
    has_won = models.NullBooleanField('Has Won')

    created = models.DateTimeField('Created at', auto_now_add=True)
    updated = models.DateTimeField('Updated at', auto_now=True)

    @property
    def profit(self):
        return (self.odds - 1) * self.stake

    @property
    def returning(self):
        return self.odds * self.stake
