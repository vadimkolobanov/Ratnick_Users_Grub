from telethon.tl.types import PeerUser, PeerChannel, UserStatusOffline, UserStatusOnline, UserProfilePhoto, \
    UserProfilePhotoEmpty


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


class UserProcessor:
    def __init__(self, user):
        self.user = user

    def get_user_id(self):
        return self.user.id

    def get_access_hash(self):
        return self.user.access_hash

    def get_first_name(self):
        return self.user.first_name

    def get_last_name(self):
        return self.user.last_name

    def get_username(self):
        return self.user.username

    def get_phone(self):
        return self.user.phone

    def get_photo_id(self):
        if self.user.photo and  not isinstance(self.user.photo, UserProfilePhotoEmpty):
            return self.user.photo.photo_id
        else:
            return None

    def get_status(self):
        if isinstance(self.user.status, UserStatusOffline):
            return "Offline"
        elif isinstance(self.user.status, UserStatusOnline):
            return "Online"
        else:
            return None


def process_messages(message_list):
    for message in message_list:
        processor = MessageProcessor(message)
        message_id = processor.get_message_id()
        sender_id = processor.get_sender_id()
        message_text = processor.get_message_text()


def process_users(user_list, channel_data,database_instance):
    database_instance.connect()
    for user_data in user_list:
        processor = UserProcessor(user_data)
        user_id = processor.get_user_id()
        access_hash = processor.get_access_hash()
        first_name = processor.get_first_name()
        last_name = processor.get_last_name()
        username = processor.get_username()
        phone = processor.get_phone()
        photo_id = processor.get_photo_id()
        status = processor.get_status()
        channel_id = channel_data.id
        database_instance.insert_user(user_id,access_hash,first_name,last_name,username,phone,photo_id,status,channel_id)

        print(user_id, access_hash, first_name, last_name, username, phone, photo_id, status, channel_id)
