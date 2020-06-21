from Betty.apps.bets.models import Bet


class BettingService:
    @staticmethod
    def find_matching_bet(bet):
        return Bet.objects.filter(
            event=bet.event, selection=bet.selection,
            matched=False
        ).exclude(side=bet.side).first()

    @staticmethod
    def match_bets(bet):
        matching_bet = BettingService.find_matching_bet(bet)
        if matching_bet is None:
            return

        Bet.objects.filter(pk=bet.pk).update(
            matching_bet=matching_bet, matched=True
        )
        Bet.objects.filter(pk=matching_bet.pk).update(
            matching_bet=bet, matched=True
        )
