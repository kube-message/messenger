from ..models import session, Message


def get_message_by_id(message_id):
    return session.query(Message).get(message_id)


def get_messages_for_thread(thread_id):
    return session.query(Message).filter_by(thread_id=thread_id)


def send_message(thread_id, sender_id, text):
    try:
        message = Message(thread_id=thread_id, sender_id=sender_id, text=text)
        session.add(message)
        session.commit()
        return message
    except Exception as err:
        print("error sending message: %s" % err)
