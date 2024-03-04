import sqlite3


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        # Подключение к базе данных
        self.connection = sqlite3.connect(self.db_name)

    def create_tables(self):
        # Создание таблиц
        cursor = self.connection.cursor()

        # Создание таблицы "Users"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                access_hash TEXT,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                phone TEXT,
                photo_id INTEGER,
                status TEXT,
                channel_id INTEGER,
                FOREIGN KEY (photo_id) REFERENCES ProfilePhotos(id),
                FOREIGN KEY (channel_id) REFERENCES Channels(id)
            )
        ''')

        # Создание таблицы "ProfilePhotos"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ProfilePhotos (
                id INTEGER PRIMARY KEY,
                file_path TEXT,
                other_details TEXT
            )
        ''')

        # Создание таблицы "Channels"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Channels (
                id INTEGER PRIMARY KEY,
                name TEXT,
                link TEXT
            )
        ''')

        # Создание таблицы "Messages"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Messages (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                channel_id INTEGER,
                date DATETIME,
                message TEXT,
                out INTEGER,
                mentioned INTEGER,
                media_unread INTEGER,
                silent INTEGER,
                post INTEGER,
                reply_to INTEGER,
                views INTEGER,
                forwards INTEGER,
                FOREIGN KEY (user_id) REFERENCES Users(id),
                FOREIGN KEY (channel_id) REFERENCES Channels(id),
                FOREIGN KEY (reply_to) REFERENCES Messages(id)
            )
        ''')

        self.connection.commit()

    def execute_query(self, query, *args):
        # Исполнение SQL-запроса
        cursor = self.connection.cursor()
        cursor.execute(query, args)
        self.connection.commit()

    def insert_user(self, user_id, access_hash, first_name, last_name, username, phone, photo_id, status, channel_id):
        query = '''
            INSERT OR IGNORE INTO Users (id, access_hash, first_name, last_name, username, phone, photo_id, status, channel_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        cursor = self.connection.cursor()
        cursor.execute(query,
                       (user_id, access_hash, first_name, last_name, username, phone, photo_id, status, channel_id))
        self.connection.commit()



    def close(self):
        # Закрытие соединения с базой данных
        self.connection.close()
