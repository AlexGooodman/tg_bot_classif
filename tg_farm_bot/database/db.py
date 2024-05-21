import sqlite3 as sq
from typing import Union

def get_len_users():
    """Возвращает число всех юзеров из бд"""
    with sq.connect('database/storage/database.db') as con:
        cur = con.cursor()
    cur.execute("SELECT user_id FROM users_info")
    len_users = len(cur.fetchall())
    return len_users

def get_all_users_for_txt():
    """Формирует документ со списком всех юзеров из бд"""
    with sq.connect('database/storage/database.db') as con:
        cur = con.cursor()
    cur.execute("SELECT user_id, user_name FROM users_info")
    with open("files/users.txt",'w', encoding="utf-8") as file:
        users = cur.fetchall()
        for user in users:
            file.write(f'{user[0]}: {user[1]}\n')

def get_users_id():
    """Получает все user_id из бд"""
    with sq.connect('database/storage/database.db') as con:
        cur = con.cursor()
    cur.execute("SELECT user_id FROM users_info")
    users = cur.fetchall()
    users_list = []
    for user in users:
        users_list.append(user[0])
    return users_list

def get_title_from_data(rowid):
    """Получает имя классификаций из бд"""
    with sq.connect('database/storage/database.db') as con:
        cur = con.cursor()
    cur.execute(f"SELECT topic_title FROM classifications WHERE ROWID={rowid}")
    try:
        return ('').join(cur.fetchone())
    except TypeError:
        return False

def show_choice_classif(numb1, numb2):
    """Показывает имя выбранных нескольких классификаций"""
    with sq.connect('database/storage/database.db') as con:
        cur = con.cursor()
    cur.execute(f"SELECT topic_title FROM classifications WHERE ROWID>={numb1} and ROWID<={numb2}")
    all_line = cur.fetchall()
    finally_string = []
    for line in all_line:
        finally_string.append(f'{line[0]}')
    return (', ').join(finally_string)

def show_choice_random_classif(rowid):
    """Показывает имя выбранных нескольких классификаций"""
    with sq.connect('database/storage/database.db') as con:
        cur = con.cursor()
    cur.execute(f"SELECT topic_title FROM classifications WHERE ROWID in ({rowid})")
    all_line = cur.fetchall()
    finally_string = []
    for line in all_line:
        finally_string.append(f'{line[0]}')
    return (', ').join(finally_string)

def get_path_to_file(rowid):
    """Принимает id классификации, возвращает путь к файлу нужной классиф"""
    try:
        with sq.connect('database/storage/database.db') as con:
            cur = con.cursor()
        cur.execute(f"SELECT file_path FROM classifications WHERE ROWID={rowid}")
        return ('').join(cur.fetchone())
    except TypeError:
        return False
    
def get_path_to_many_files(numb1, numb2):
    """Принимает id классификаций(с тире), возвращает путь к файлу нужных классиф"""
    try:
        with sq.connect('database/storage/database.db') as con:
            cur = con.cursor()
        cur.execute(f"SELECT file_path FROM classifications WHERE ROWID>={numb1} and ROWID<={numb2}")
        all_line = cur.fetchall()
        finally_string = []
        for line in all_line:
            finally_string.append(f'{line[0]}')
        if len(finally_string) != 0:
            return finally_string
        else:
            return False
    except TypeError:
        return False

def get_path_to_many_random_files(rowid):
    """Принимает id классификаций(через запятую), возвращает путь к файлу нужных классиф"""
    try:
        with sq.connect('database/storage/database.db') as con:
            cur = con.cursor()
        cur.execute(f"SELECT file_path FROM classifications WHERE ROWID in ({rowid})")
        all_line = cur.fetchall()
        finally_string = []
        for line in all_line:
            finally_string.append(f'{line[0]}')
        if len(finally_string) != 0:
            return finally_string
        else:
            return False
    except TypeError:
        return False
    

def get_all_titles_from_data():
    """Получает список всех классификаций из бд"""
    with sq.connect('database/storage/database.db') as con:
        cur = con.cursor()
    cur.execute("SELECT topic_title FROM classifications")
    all_line = cur.fetchall()
    finally_string = []
    for num, line in enumerate(all_line):
        num += 1
        finally_string.append(f'{num}: {line[0]}\n')
    return ('').join(finally_string)

def save_user_in_bd(user_id: int, name: str):
    """Сохраняет user_id и name в бд"""
    with sq.connect('database/storage/database.db') as con:
        cur = con.cursor()
        cur.execute(f"INSERT OR IGNORE INTO users_info (user_id, user_name) VALUES ({user_id}, '{name}')")


def save_line_for_user_favourites(user_id: int, key: str, value: str):
    """Сохраняет выбранную строчку в избранное(бд)"""
    with sq.connect('database/storage/database.db') as con:
        cur = con.cursor()
        cur.execute(f"INSERT OR IGNORE INTO favourites VALUES ({user_id}, '{key}', '{value}')")

def delete_line_from_bd(user_id: int, key: str):
    """Удаляет выбранную строчку из избранного(бд)"""
    with sq.connect('database/storage/database.db') as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM favourites WHERE key='{key}' AND users={user_id}")

def delete_all_user_line_from_bd(user_id: int):
    """Очищает все сохранненные строчки юзера из бд"""
    with sq.connect('database/storage/database.db') as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM favourites WHERE users={user_id}")

def get_user_favourites_in_bd(user_id: int) -> Union[dict, None]:
    """Получает сохраненные строчки юзера из бд"""
    with sq.connect('database/storage/database.db') as con:
        cur = con.cursor()
    cur.execute(f"SELECT key, value FROM favourites WHERE users = {user_id}")
    result = cur.fetchall()
    finally_result = {}
    if len(result) != 0:
        for line in result:
            finally_result[line[0]] = line[1]
        return finally_result
    else:
        return None


# async def save_user_favourites_in_bd(user_id: int, favourites: dict):
#     with sq.connect('database/storage/database.db') as con:
#         json_favourites = json.dumps(favourites)
#         cur = con.cursor()
#         cur.execute(f"UPDATE favourites SET user_favourites = '{json_favourites}' WHERE user_id = {user_id}")

# def get_user_favourites_in_bd(user_id: int) -> dict:
#     with sq.connect('database/storage/database.db') as con:
#         cur = con.cursor()
#     cur.execute(f"SELECT user_favourites FROM favourites WHERE user_id = {user_id}")
#     result = json.loads(cur.fetchone()[0])
#     return result
