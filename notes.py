"""
Main menu and user interface for notebook app
"""

from utils import (
    Note,
    note_insert,
    notes_list,
    note_delete,
    note_change,
    note_show,
)

from settings import (
    SEPARATOR,
    MAIN_MENU_ITEMS,
    APP_TITLE,
    APP_VERSION,
    APP_INTRO,
    INCORRECT_MENU_ITEM,
    INCORRECT_USER_ID,
    NO_USER_ID,
    INCORRECT_NOTE_ID,
)

is_exit = False
user_id = -1

print("\n", APP_TITLE, APP_VERSION)
print(APP_INTRO, "\n")

while not is_exit:
    # main menu
    print(SEPARATOR)
    for key, value in MAIN_MENU_ITEMS.items():
        print(key + " - " + value)
    option = input('---\nВведите номер пункта меню: ')
    if not option.isdigit():
        option = -1
    else:
        option = int(option)
    if option == 0:
        is_exit = True
    elif option == 1:
        user_id = input('---\nВведите идентификатор пользователя: ')
        if not user_id.isdigit():
            print(INCORRECT_USER_ID)
            user_id = -1
        else:
            user_id = int(user_id)
    elif option == 2:
        if user_id >= 0:
            notes_list(user_id)
        else:
            print(NO_USER_ID)
    elif option == 3:
        if user_id >= 0:
            title = input("Введите заголовок заметки: ")
            content = input("Введите текст заметки: ")
            note = Note(user_id, title, content)
            result = note_insert(note)
            if result == 0:
                print("Заметка № ", note.id, "успешно создана.")
        else:
            print(NO_USER_ID)
    elif option == 4:
        if user_id >= 0:
            note_id = input("Введите номер заметки: ")
            if note_id.isdigit():
                note_show(int(note_id), user_id)
            else:
                print(INCORRECT_NOTE_ID)
        else:
            print(NO_USER_ID)
    elif option == 5:
        if user_id >= 0:
            note_id = input("Введите номер заметки: ")
            result = note_show(int(note_id), user_id)
            if result == 0:
                if note_id.isdigit():
                    title = input("Введите новый заголовок заметки или оставьте поле пустым, "
                                  "если его редактировать не нужно: ")
                    content = input("Введите новый текст заметки или оставьте поле пустым, "
                                    "если его редактировать не нужно: ")
                    result = note_change(int(note_id), user_id, title=title, content=content)
                    if result == 0:
                        print("Заметка №", note_id, "успешно изменена.")
                else:
                    print(INCORRECT_NOTE_ID)
        else:
            print(NO_USER_ID)
    elif option == 6:
        if user_id >= 0:
            note_id = input("Введите номер заметки: ")
            result = note_show(int(note_id), user_id)
            if result == 0:
                if note_id.isdigit():
                    result = note_delete(int(note_id))
                    if result == 0:
                        print("Заметка №", note_id, "успешно удалена.")
                else:
                    print(INCORRECT_NOTE_ID)
        else:
            print(NO_USER_ID)
    else:
        print(INCORRECT_MENU_ITEM)
