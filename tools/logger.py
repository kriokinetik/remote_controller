import logging

logger = logging.getLogger("remote_controller")


def logger_event_info(event):
    username = event.from_user.username
    user_id = event.from_user.id
    content = event.text if hasattr(event, "text") else event.data
    logging.info(f"Received event from @{username} id={user_id} — '{content}'")


def logger_info(text: str):
    logging.info(text)


def logger_error(exception, exc_info=False):
    logging.error(str(exception), exc_info=exc_info)
