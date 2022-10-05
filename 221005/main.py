from datetime import datetime
import re
from collections import namedtuple
import sqlite3

Question = namedtuple('Question', 'idn date_and_time text sender answered comments')
Answer = namedtuple('Answer', 'idn date_and_time text sender')


def login(cur):
    while 1:
        n_name = input('Name:\n')
        flag = cur.execute(f"SELECT password FROM users WHERE username = '{n_name}'")
        if flag.fetchone() is None:
            print('Username does not exist!')
        else:
            break
    while 1:
        n_password = input('Password:\n')
        success = cur.execute(f"SELECT password FROM users WHERE username='{n_name}' AND password = '{n_password}'")
        if success.fetchone() is None:
            print('Incorrect password')
        else:
            break
    return n_name


def signup(conn, cur):
    while 1:
        n_name = input('Name:\n')
        flag = cur.execute('SELECT * FROM users WHERE username=?', (n_name,))
        if flag.fetchone() is None:
            break
        else:
            print('Username already exists!')
    while 1:
        n_password = input('Password:\n')
        rpt = input('Repeat password:\n')
        if n_password == rpt:
            break
        else:
            print('Passwords are not the same!\n')
    cur.execute(f"""INSERT INTO users(username, password)
        VALUES('{n_name}', '{n_password}')""")
    conn.commit()
    return n_name


def answer_question(qid, usr, conn, cur):
    n_time = datetime.now()
    n_text = input('Answer:\n')

    cur.execute(f"""INSERT INTO answers(question_id, time, sender, text)
        VALUES('{qid}', '{str(n_time)}', '{usr}', '{n_text}')""")
    conn.commit()


def new_question(usr, conn, cur):
    qid = ''
    answered = 'New'
    date_and_time = datetime.now()
    n_text = input('Your question:\n')
    time_list = re.findall(r'\d', str(date_and_time))
    for i in time_list:
        qid += i
    qid += usr[0].lower()

    cur.execute(f"""INSERT INTO questions(question_id, time, sender, text, status)
        VALUES('{qid}', '{str(date_and_time)}', '{usr}', '{n_text}', '{answered}')""")
    conn.commit()


def print_quest(quest):
    print(f'id: {quest.idn}\nTime: {quest.date_and_time}\nSender: {quest.sender}\n'
          f'Answered: {quest.answered}\nQuestion:\n{quest.text}\nComments:\n{quest.comments}\n')


def print_ans(ans):
    print(f'id: {ans.idn}\nTime: {ans.date_and_time}\nSender: {ans.sender}\n'
          f'Answer:\n{ans.text}\n')


def fetch_questions(cur):
    dict_of_questions = {}
    query = cur.execute('SELECT * FROM questions')
    questions = query.fetchall()
    for quest in questions:
        dict_of_questions.update({quest[0]: Question(idn=quest[0], date_and_time=quest[1], sender=quest[2],
                                                     answered=quest[4], comments=quest[5], text=quest[3])})
    return dict_of_questions


def fetch_answers(cur):
    dict_of_answers = {}
    query = cur.execute('SELECT * FROM answers')
    answers = query.fetchall()
    for ans in answers:
        dict_of_answers.update({ans[0]: Answer(idn=ans[0], date_and_time=ans[1], sender=ans[2],
                                               text=ans[3])})
    return dict_of_answers


def show_new_questions(cur):
    dict_of_questions = fetch_questions(cur)
    sorted_questions = dict(sorted(dict_of_questions.items()))
    for quest in sorted_questions.values():
        if quest.answered == 'New':
            print_quest(quest)
            print('====================================\n')


def show_answered(cur):
    dict_of_quest = fetch_questions(cur)
    dict_of_ans = fetch_answers(cur)
    sorted_questions = dict(sorted(dict_of_quest.items()))
    for qid, quest in sorted_questions.items():
        if qid in dict_of_ans.keys():
            print_quest(quest)
            print('------------------------------------\n')
            print_ans(dict_of_ans[qid])
            print('====================================\n')


def show_all_questions(cur):
    dict_of_questions = fetch_questions(cur)
    sorted_questions = dict(sorted(dict_of_questions.items()))
    for quest in sorted_questions.values():
        print_quest(quest)
        print('====================================\n')


def show_all_answers(cur):
    dict_of_ans = fetch_answers(cur)
    sorted_answers = dict(sorted(dict_of_ans.items()))
    for ans in sorted_answers.values():
        print_ans(ans)
        print('====================================\n')


def dbconnect():
    conn = sqlite3.connect('messenger.db')
    cur = conn.cursor()
    # Users
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    );""")
    conn.commit()
    # Questions
    cur.execute("""CREATE TABLE IF NOT EXISTS questions(
        question_id TEXT PRIMARY KEY,
        time TEXT,
        sender TEXT,
        text TEXT,
        status TEXT,
        comments TEXT
    );""")
    conn.commit()
    # Answers
    cur.execute("""CREATE TABLE IF NOT EXISTS answers(
        question_id TEXT PRIMARY KEY,
        time TEXT,
        sender TEXT,
        text TEXT
    );""")
    conn.commit()
    return conn, cur


if __name__ == '__main__':
    db, cursor = dbconnect()
    ch = int(input('Press 0 to login, 1 to sign up:\n'))
    c_user = None
    while not c_user:
        if ch == 0:
            c_user = login(cur=cursor)
        if ch == 1:
            c_user = signup(conn=db, cur=cursor)
    while 1:
        choice = int(input('Press 0 to exit, 1 to read, 2 to ask, 3 to answer:\n'))
        if choice == 0:
            break
        if choice == 1:
            ch1 = int(input('Press 0 to exit, 1: all questions, 2: all answers, 3: new, 4: answered\n'))
            if ch1 == 0:
                pass
            if ch1 == 1:
                show_all_questions(cursor)
            if ch1 == 2:
                show_all_answers(cursor)
            if ch1 == 3:
                show_new_questions(cursor)
            if ch1 == 4:
                show_answered(cursor)
        if choice == 2:
            new_question(usr=c_user, conn=db, cur=cursor)
        if choice == 3:
            while 1:
                answer_id = input('Question ID:\n')
                exist = cursor.execute(f"SELECT * FROM questions WHERE question_id = '{answer_id}'")
                if exist.fetchone() is not None:
                    cursor.execute(f'UPDATE questions SET status = "Answered" WHERE question_id = "{answer_id}"')
                    answer_question(answer_id, c_user, db, cursor)
                    db.commit()
                    break
                else:
                    print('Incorrect question id')
                break
