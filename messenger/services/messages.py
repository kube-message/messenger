from ..models import session, Message
from ..proto import messenger
from ..utils import get_logger


logger = get_logger()


def to_proto(message):
    return messenger.Message(
        id=message.pk,
        sender_id=message.sender_id,
        thread_id=message.thread_id,
        text=message.text,
    )


def from_proto(message_proto):
    return Message(
        pk=message_proto.id,
        sender_id=message_proto.sender_id,
        thread_id=message_proto.thread_id,
        text=message_proto.text,
    )


def get_message_by_id(message_id):
    """
    Get a single message by it's id.

    Args:
        message_id (int, long): The ID of the message.

    Returns:
        Message
    """
    try:
        return session.query(Message).get(message_id)
    except Exception as err:
        logger.error("error fetching message: %s", err)
        return None


def get_messages_for_thread(thread_id):
    try:
        return session.query(Message).filter_by(thread_id=thread_id)
    except Exception as err:
        logger.error("error fetching messages for thread: %s", err)
        return None


def send_message(thread_id, sender_id, text):
    try:
        message = Message(thread_id=thread_id, sender_id=sender_id, text=text)
        session.add(message)
        session.commit()
        return message
    except Exception as err:
        logger.error("error saving message: %s", err)
        return None
