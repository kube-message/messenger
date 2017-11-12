import os
from time import time

import grpc

from ..proto import alerts
from ..services import threads
from ..utils import get_logger


logger = get_logger()
_client = None


def get_alerts_addr():
    return "{}:{}".format(
        os.environ.get("ALERTS_SERVICE_HOST", "localhost"),
        os.environ.get("ALERTS_SERVICE_PORT", 8081)
    )


def _get_alerts_client():
    global _client
    if _client is None:
        channel = grpc.insecure_channel(get_alerts_addr())
        _client = alerts.AlertsStub(channel)
    return _client


def send_alert_for_message(recipient_id, thread_id):
    try:
        client = _get_alerts_client()
        alert = alerts.Alert(
            recipient_id=recipient_id,
            thread_id=thread_id,
            message="New message",
            timestamp=str(int(time())),
            action_path="/threads/{}/messages".format(thread_id)
        )
        request = alerts.SendAlertRequest(alert=alert)
        logger.info("Sending alert for user:%s on thread:%s", recipient_id, thread_id)
        response = client.SendAlert(request)
        return response
    except Exception as err:
        logger.error("error calling alerts service: %s", err)
        return alerts.SendAlertResponse(error=alerts.AlertError(message="error sending alert: %s" % err))


def send_alerts_for_thread_participants(thread_id):
    try:
        resposnes = []
        participant_ids = threads.get_thread_participant_ids(thread_id)
        for participant_id in participant_ids:
            response = send_alert_for_message(participant_id, thread_id)
            resposnes.append(response)
        return resposnes
    except Exception as err:
        logger.error("an error occured during alert sending: %s", err)
