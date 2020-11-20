from datetime import datetime
from ApiGateway.clients.utils import _get, _post, _patch
import datetime

NOTIFICATIONS_SERVICE = "http://notifications.local:8080/"

def get_notification(id):
    return _get(f"{NOTIFICATIONS_SERVICE}/notifications/{id}")

def get_notifications(user_id, read=None):
    url = f"{NOTIFICATIONS_SERVICE}/notifications?user_id={user_id}"
    if read is not None:
        url += f"&read={'true' if read else 'false'}"

    return _get(url)

def create_notification(user_id, content):
    data = {
        "user_id": user_id,
        "content": content,
        "sent_on": datetime.now().isoformat()
    }
    url = f"{NOTIFICATIONS_SERVICE}/notifications"
    return _post(url, data)

def mark_notification_as_read(id):
    data = {
        "read_on": datetime.now().isoformat()
    }
    url = f"{NOTIFICATIONS_SERVICE}/notifications/{id}"
    return _patch(url, data)