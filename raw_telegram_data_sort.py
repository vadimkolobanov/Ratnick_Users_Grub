from telethon.tl.types import PeerUser, PeerChannel


class MessageProcessor:
    def __init__(self, message):
        self.message = message

    def get_message_id(self):
        return self.message.id

    def get_sender_id(self):
        if isinstance(self.message.from_id, PeerUser):
            return self.message.from_id.user_id
        elif isinstance(self.message.from_id, PeerChannel):
            return self.message.from_id.channel_id
        else:
            return None

    def get_message_text(self):
        if self.message.message:
            return self.message.message


def process_messages(message_list):
    for message in message_list:
        processor = MessageProcessor(message)
        message_id = processor.get_message_id()
        sender_id = processor.get_sender_id()
        message_text = processor.get_message_text()

