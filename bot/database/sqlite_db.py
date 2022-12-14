from aiogram.types.user import User

import sqlite3 as sql
import json


def initial_db():
    global base, cur
    base = sql.connect('questionnaire_bot.db')
    cur = base.cursor()
    if base:
        print('База даних успішно під`єднана')
    base.execute('CREATE TABLE IF NOT EXISTS groups(group_id INTEGER PRIMARY KEY AUTOINCREMENT, group_name TEXT)')
    base.execute('''CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id_user INTEGER,
      full_name TEXT, group_id INTEGER, FOREIGN KEY (group_id) REFERENCES groups (group_id))''')
    base.execute('CREATE TABLE IF NOT EXISTS questionnaire(questionnaire_id INTEGER PRIMARY KEY AUTOINCREMENT, questionnaire_title TEXT, questionnaire_json TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS response(response_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, questionnaire_id INTEGER, response_json TEXT)')


def sql_new_user(user : User):
    if not cur.execute(f'SELECT user_id FROM user WHERE telegram_id_user={user.id}').fetchall():
        cur.execute(f'INSERT INTO user (telegram_id_user, full_name, group_id) VALUES (?, ?, ?)', (user.id, user.full_name, None))
        base.commit()


def sql_create_questionnaire(questionnaire):
    questionnaire_json = json.dumps(dict(questionnaire))
    cur.execute('INSERT INTO questionnaire (questionnaire_title, questionnaire_json) VALUES (?, ?)', (questionnaire['title'], questionnaire_json))
    base.commit()


def sql_get_all_questionnaires_titles():
    return cur.execute('SELECT questionnaire_title FROM questionnaire').fetchall()


def sql_get_allowed_questionnaires(user_tg_id):
    res = []
    quests = cur.execute(f'SELECT questionnaire_json FROM questionnaire').fetchall()
    group = cur.execute(f'SELECT group_name FROM groups WHERE group_id IN (SELECT group_id FROM user WHERE telegram_id_user = {user_tg_id})').fetchall()[0][0]
    for quest in quests:
        q = json.loads(quest[0])
        if not q['groups'] or group in q['groups']:
            res.append(q['title'])
    return res


def sql_get_questionnaire(questionnaire_title):
    q = cur.execute(f'SELECT questionnaire_json FROM questionnaire WHERE questionnaire_title="{questionnaire_title}"').fetchall()[0]
    return json.loads(q[0])


def sql_create_group(data):
    print(data["name"])
    cur.execute(f'INSERT INTO groups (group_name) VALUES (?)', (data['name'],))
    base.commit()


def sql_get_groups():
    return cur.execute('SELECT group_name FROM groups').fetchall()


def sql_join_user_in_group(user_tg_id, group_name):
    print(user_tg_id)
    print(group_name)
    group = cur.execute(f'SELECT group_id FROM groups WHERE group_name = "{group_name}"').fetchall()[0][0]
    print(group)
    cur.execute(f'UPDATE user SET group_id = {group} WHERE telegram_id_user = {user_tg_id}')
    base.commit()


def sql_write_resopnse(response, user : User):
    title = response['questions']['title']
    response = json.dumps(dict(response))
    id = cur.execute(f'SELECT questionnaire_id FROM questionnaire WHERE questionnaire_title = "{title}"').fetchall()[0][0]
    cur.execute(f'INSERT INTO response (user_id, questionnaire_id, response_json) VALUES (?, ?, ?)', (user.id, id, response))
    base.commit()


def sql_get_responses(title):
    id = cur.execute(f'SELECT questionnaire_id FROM questionnaire WHERE questionnaire_title = "{title}"').fetchall()[0][0]
    return cur.execute(f'SELECT response_json FROM response WHERE questionnaire_id = {id}').fetchall()


def sql_get_username(id):
    return cur.execute(f'SELECT full_name FROM user WHERE telegram_id_user = {id}').fetchall()[0][0]