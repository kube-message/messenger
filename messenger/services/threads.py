from ..models import session, Thread
from ..proto import messenger
from ..utils import get_logger


logger = get_logger()


def to_proto(thread):
    return messenger.Thread(participants=thread.participants)


def from_proto(thread_proto):
    return Thread(participants=thread_proto.participants)


def get_thread_by_id(thread_id):
    try:
        return session.query(Thread).get(thread_id)
    except Exception as err:
        logger.error("error fetching thread:%s: %s", thread_id, err)


def get_threads_for_user(user_id):
    try:
        return session.query(Thread).filter(Thread.participants.any(user_id)).all()
    except Exception as err:
        logger.error("error fetching threads for user: %s: %s", user_id, err)


def get_thread_participant_ids(thread_id):
    particiapnts = []
    thread = get_thread_by_id(thread_id)
    if thread:
        particiapnts = thread.participants
    return particiapnts


def is_user_in_thread(user_id, thread_id):
    return user_id in get_thread_participant_ids(thread_id)


def create_thread(participants):
    try:
        thread = Thread(participants=participants)
        session.add(thread)
        session.commit()
        return thread
    except Exception as err:
        logger.error("error creating thread: %s", err)
