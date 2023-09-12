"""
Utils for database records handling
"""
from datetime import datetime
from json import load, dump
from os.path import isfile

from settings import (
    DATABASE_PATH,
    FILE_NOT_FOUND,
    RECORD_NOT_FOUND,
    NO_RECORDS_FOUND,
    WRONG_USER_ID,
)


class Note:
    """
        Class for user notes
    """
    if isfile(DATABASE_PATH):
        with open(DATABASE_PATH, 'r', encoding='UTF-8') as database:
            data = load(database)
            if data:
                __id = max([int(key) for key in data.keys()])
            else:
                __id = 0
    else:
        __id = 0

    @classmethod
    def _increase_id(cls) -> int:
        cls.__id += 1
        return cls.__id

    def __init__(self, user: int, title: str, content: str):
        self.id = self._increase_id()
        self.user = user
        self.__date = datetime.now()
        self.title = title
        self.content = content
        self.__last_edited = datetime.now()

    def get_date(self):
        return self.__date

    def get_last_edited(self):
        return self.__last_edited


def note_insert(f_data: Note) -> int:
    """
    The function inserts user note into database.
    :param f_data: Note
    :return: int
    """
    try:
        data = {}
        record = {
                "user": f_data.user,
                "date": f_data.get_date().strftime("%d/%m/%y %H:%M:%S"),
                "last_edited": f_data.get_last_edited().strftime("%d/%m/%y %H:%M:%S"),
                "title": f_data.title,
                'content': f_data.content
        }
        if isfile(DATABASE_PATH):
            with open(DATABASE_PATH, 'r', encoding='UTF-8') as database:
                data = load(database)
        data[f_data.id] = record
        with open(DATABASE_PATH, 'w', encoding='UTF-8') as database:
            dump(data, database, indent=4)
        return 0
    except RuntimeError:
        return -1


def note_show(f_id: int, f_user_id: int) -> int:
    """
    The function shows user note with specific id.
    :param f_user_id: int
    :param f_id: int
    :return: int
    """
    if isfile(DATABASE_PATH):
        with open(DATABASE_PATH, 'r', encoding='UTF-8') as database:
            data = load(database)
            f_id = str(f_id)
            try:
                print("\nID: " + f_id + ":")
                if data[f_id]["user"] == f_user_id:
                    for item, value in data[f_id].items():
                        print(item, " = ", value)
                else:
                    print(WRONG_USER_ID)
                    return -1
            except KeyError:
                print(RECORD_NOT_FOUND)
                return -1
        with open(DATABASE_PATH, 'w', encoding='UTF-8') as database:
            dump(data, database, indent=4)
            return 0
    else:
        print(FILE_NOT_FOUND)
        return -1


def note_change(f_note_id: int, f_user_id: int, title: str = None, content: str = None) -> int:
    """
    The function changes user note with specific id.
    :param f_user_id: int
    :param content: str
    :param title: str
    :param f_note_id: int
    :return: int
    """

    if isfile(DATABASE_PATH):
        with open(DATABASE_PATH, 'r', encoding='UTF-8') as database:
            data = load(database)
            f_note_id = str(f_note_id)
            if data[f_note_id]["user"] != f_user_id:
                print(WRONG_USER_ID)
            else:
                try:
                    if title:
                        data[f_note_id]["title"] = title
                    if content:
                        data[f_note_id]["content"] = content
                except KeyError:
                    print(RECORD_NOT_FOUND)
                    return -1
        with open(DATABASE_PATH, 'w', encoding='UTF-8') as database:
            dump(data, database, indent=4)
        return 0
    else:
        print(FILE_NOT_FOUND)
        return -1


def note_delete(f_id: int) -> int:
    """
    The function delete user note from database.
    :param f_id: int
    :return: int
    """
    if isfile(DATABASE_PATH):
        with open(DATABASE_PATH, 'r', encoding='UTF-8') as database:
            data = load(database)
            try:
                data.pop(str(f_id))
            except KeyError:
                print(RECORD_NOT_FOUND)
                return -1
        with open(DATABASE_PATH, 'w', encoding='UTF-8') as database:
            dump(data, database, indent=4)
        return 0
    else:
        print(FILE_NOT_FOUND)
    return -1


def notes_list(f_user_id: int) -> None:
    """
    The function shows all user notes from notes.json.
    :param f_user_id: int
    :return: None
    """

    if isfile(DATABASE_PATH):
        with open(DATABASE_PATH, 'r', encoding='UTF-8') as database:
            data = load(database)
            found = False
            for key in data.keys():
                if data[key]["user"] == f_user_id:
                    found = True
                    print("\nID: " + key + ":")
                    for item, value in data[key].items():
                        print(item, " = ", value)
            if not found:
                print("Пользователь:", f_user_id, NO_RECORDS_FOUND)
    else:
        print(FILE_NOT_FOUND)
