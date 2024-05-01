import requests
from typing import Callable


def get_notify() -> Callable[[str, str], str]:
    def notify(email: str, message: str) -> str:
        resp = requests.post(
            "http://0.0.0.0:8001/notify",
            json={"recipient_email": email, "message": message},
        )

        notification_status = resp.json()
        return notification_status["status"]

    return notify
