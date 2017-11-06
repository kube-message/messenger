from ..models import session, Thread


def get_thread_by_id(thread_id):
    return session.query(Thread).get(thread_id)


def get_threads_for_user(user_id):
    return session.query(Thread).filter(Thread.participants.any(user_id)).all()


def is_user_in_thread(user_id, thread_id):
    thread = session.query(Thread).get(thread_id)
    if thread:
        return user_id in thread.participants
    return False


def create_thread(participants):
    try:
        thread = Thread(participants=participants)
        session.add(thread)
        session.commit()
        return thread
    except Exception as err:
        print("error creating thread: %s" % err)
