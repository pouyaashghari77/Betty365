from django.db import models


class Event(models.Model):
    RESULT_HOME_WIN = 'Home Win'
    RESULT_AWAY_WIN = 'Away Win'
    RESULT_DRAW = 'Draw'
    RESULT_UPCOMING = 'Upcoming'
    RESULT_CHOICES = (
        (RESULT_HOME_WIN, 'Home Win'),
        (RESULT_AWAY_WIN, 'Away Win'),
        (RESULT_DRAW, 'Draw'),
        (RESULT_UPCOMING, 'Upcoming')
    )
    title = models.CharField('Title', max_length=64)
    slug = models.SlugField('Slug', max_length=64)
    home = models.CharField('Home', max_length=64)
    away = models.CharField('Away', max_length=64)
    home_odds = models.FloatField('Home Odds')
    away_odds = models.FloatField('Away Odds')
    draw_odds = models.FloatField('Draw Odds')
    date = models.DateTimeField('Date')
    result = models.CharField('Result', max_length=32,
                              choices=RESULT_CHOICES, default=RESULT_UPCOMING,
                              blank=True, null=True)

    created = models.DateTimeField('Created at', auto_now_add=True)
    updated = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f'{self.home} - {self.away}'


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


class Deposit(models.Model):
    serial_num = models.CharField('Serial Number', max_length=128, null=True, blank=True)
    code = models.CharField('Code', max_length=128, null=True, blank=True)
    amount = models.FloatField('Amount', default=0, null=True, blank=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,
                             related_name='deposits',
                             null=True, blank=True,
                             verbose_name='User')

    created = models.DateTimeField('Created at', auto_now_add=True)
    updated = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        verbose_name = 'Deposit'
        verbose_name_plural = 'Deposits'


class WithdrawalRequest(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_APPROVED = 'Approved'
    STATUS_CANCELLED = 'Cancelled'
    STATUS_REJECTED = 'Rejected'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_REJECTED, 'Rejected'),
    )
    amount = models.FloatField('Amount', default=0, null=True, blank=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,
                             null=True, blank=True, related_name='withdrawal_requests',
                             verbose_name='User')
    status = models.CharField('Status', choices=STATUS_CHOICES, default=STATUS_PENDING,
                              max_length=32, blank=True, null=True)
    created = models.DateTimeField('Created at', auto_now_add=True)
    updated = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        verbose_name = 'Withdrawal Request'
        verbose_name_plural = 'Withdrawal Requests'
