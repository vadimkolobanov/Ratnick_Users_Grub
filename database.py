import logging
import sqlite3
from sqlite3 import IntegrityError

import psycopg2
import psycopg2.errors


class Database:
    def __init__(self, db_name, host, port, user, passwd):
        self.db_name = db_name
        self.host = host
        self.connection = None
        self.port = port
        self.user = user
        self.passwd = passwd

    def connect(self):
        # Подключение к базе данных
        self.connection = psycopg2.connect(
            host="85.234.107.159",
            database="default_db",
            user="gen_user",
            password="<-Xh1whkm;c@mb"
        )

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
                FOREIGN KEY (channel_id) REFERENCES Channels(id),
                UNIQUE (channel_id, id)
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
                link TEXT,
                date_created DATETIME
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
                FOREIGN KEY (reply_to) REFERENCES Messages(id),
                UNIQUE (channel_id, id)
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
               INSERT INTO general_users (id, access_hash, first_name, last_name, username, phone, status, channel_id_id)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO NOTHING
           '''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query,
                           (user_id, access_hash, first_name, last_name, username, phone, status, channel_id))
            self.connection.commit()
        except IntegrityError as e:
            logging.warning(f'Обнаружено дублирование значений: {e}')
            self.connection.rollback()

    def close(self):
        if self.connection:
            self.connection.close()

    def insert_channel(self, channel_id, name, link, date_created):
        query = '''
            INSERT INTO general_channels (channel_identifier, name, link, date_created)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (channel_identifier) DO NOTHING
        '''
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (channel_id, name, link, date_created))
            self.connection.commit()
        except IntegrityError as e:
            logging.warning(f'Обнаружено дублирование значений: {e}')
            self.connection.rollback()

    def user_exists(self, user_id):
        query = 'SELECT 1 FROM general_users WHERE id = %s'
        cursor = self.connection.cursor()
        cursor.execute(query, (user_id,))
        return cursor.fetchone() is not None

    def get_target(self):
        query = 'SELECT link FROM general_targetsource WHERE completed = FALSE'
        cursor = self.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        if data:
            return data[0]
        else: return None

    def get_channel_for_update_raw(self):
        query = '''
        SELECT link 
        FROM general_channels 
        WHERE last_users_updated IS NULL 
           OR last_users_updated = (SELECT MIN(last_users_updated) FROM general_channels)
        LIMIT 1
        '''
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                return row[0]
        return None

    def close_target(self, link):
        query = 'UPDATE general_targetsource SET completed = TRUE WHERE link = %s AND completed = FALSE'
        cursor = self.connection.cursor()
        cursor.execute(query, (link,))
        self.connection.commit()
        return cursor.rowcount
    def insert_message(self, message_id, user_id, channel_id, date, message, out, mentioned, media_unread, silent, post,
                       reply_to, views, forwards):
        if not self.user_exists(user_id):
            return

        query = '''
            INSERT INTO general_messages (id, user_id_id, channel_id_id, date, message, out, mentioned, media_unread, silent, post, reply_to, views, forwards)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        '''
        date_str = date.strftime('%Y-%m-%d %H:%M:%S')

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (
                message_id, user_id, channel_id, date_str, message, out, mentioned, media_unread, silent, post,
                reply_to,
                views, forwards))
            self.connection.commit()
        except psycopg2.IntegrityError as e:
            logging.warning(f'Обнаружено дублирование значений: {e}')
            self.connection.rollback()

    def close(self):
        # Закрытие соединения с базой данных
        self.connection.close()
