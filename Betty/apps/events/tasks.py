from billiard.exceptions import SoftTimeLimitExceeded

from Betty import celery_app

import logging

logger = logging.getLogger(__name__)


@celery_app.task(
    name='Update Upcoming Events',
    routing_key='default',
    soft_time_limit=3600,
    time_limit=3600
)
def update_upcoming_events():
    from Betty.apps.events.bwin import BWin  # NOQA

    bwin = BWin()
    try:
        bwin.updateUpcomingEvents()
    except SoftTimeLimitExceeded as exc:
        logger.exception('Soft time limit while updating upcoming events.')
        raise update_upcoming_events.retry(exc=exc)


@celery_app.task(
    name='Set Live Events',
    routing_key='default',
    soft_time_limit=3600,
    time_limit=3600
)
def set_live_events():
    from Betty.apps.events.bwin import BWin  # NOQA

    bwin = BWin()
    try:
        bwin.updateLiveEvents()
    except SoftTimeLimitExceeded as exc:
        logger.exception('Soft time limit while setting live events.')
        raise set_live_events.retry(exc=exc)


@celery_app.task(
    name='Set Concluded Events Result',
    routing_key='default',
    soft_time_limit=3600,
    time_limit=3600
)
def set_concluded_events_result():
    from Betty.apps.bets.models import Event  # NOQA
    from Betty.apps.events.bwin import BWin  # NOQA

    bwin = BWin()
    try:
        bwin.setConcludedEventsResult()
    except SoftTimeLimitExceeded as exc:
        logger.exception('Soft time limit while setting events result.')
        raise set_concluded_events_result.retry(exc=exc)
