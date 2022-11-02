from datetime import datetime
import re
from collections import namedtuple
import sqlite3
from tkinter import *
from tkinter import messagebox

Question = namedtuple('Question', 'idn date_and_time text sender answered comments')
Answer = namedtuple('Answer', 'idn date_and_time text sender')

CONN = None
CUR = None
C_USER = None


def login():
    global C_USER
    n_name = entry_username.get()
    flag = CUR.execute(f"SELECT password FROM users WHERE username = '{n_name}'")
    if flag.fetchone() is None:
        messagebox.showinfo('Error', 'Username does not exist!')
        entry_username.delete("0", END)
        entry_pwd.delete("0", END)
        return

    else:
        n_password = entry_pwd.get()
        success = CUR.execute(f"SELECT password FROM users WHERE username='{n_name}' AND password = '{n_password}'")
        if success.fetchone() is None:
            messagebox.showinfo('Error', 'Incorrect password')
            entry_pwd.delete("0", END)
            return
        else:
            entry_pwd.delete("0", END)
            C_USER = n_name
            messagebox.showinfo('Hello', f'Hello, {C_USER}')


def signup():
    global C_USER
    n_name = entry_username.get()
    flag = CUR.execute('SELECT * FROM users WHERE username=?', (n_name,))
    if flag.fetchone() is not None:
        messagebox.showinfo('Error', 'Username already exists!')
        entry_pwd.delete("0", END)
        entry_username.delete("0", END)
        return
    else:
        n_password = entry_pwd.get()
        CUR.execute(f"""INSERT INTO users(username, password)
            VALUES('{n_name}', '{n_password}')""")
        CONN.commit()
        C_USER = n_name
        entry_pwd.delete("0", END)
        messagebox.showinfo('Hello', f'Hello, {C_USER}')


def answer_question():
    n_time = datetime.now()
    n_text = entry_new_text.get()
    qid = entry_qid.get()
    answered = "Answered"

    CUR.execute(f"""INSERT INTO answers(question_id, time, sender, text)
        VALUES('{qid}', '{str(n_time)}', '{C_USER}', '{n_text}')""")

    CUR.execute(f"""UPDATE questions SET status='{answered}' WHERE question_id='{qid}'""")

    entry_new_text.delete("0", END)
    entry_qid.delete("0", END)
    CONN.commit()


def new_question():
    global C_USER
    qid = ''
    answered = 'New'
    date_and_time = datetime.now()
    n_text = entry_new_text.get()
    time_list = re.findall(r'\d', str(date_and_time))
    for i in time_list:
        qid += i
    qid += C_USER[0].lower()

    CUR.execute(f"""INSERT INTO questions(question_id, time, sender, text, status)
        VALUES('{qid}', '{str(date_and_time)}', '{C_USER}', '{n_text}', '{answered}')""")
    messagebox.showinfo('OK', f'Thank you, {C_USER}')
    entry_new_text.delete("0", END)
    CONN.commit()


def print_quest(quest):
    text = (f'id: {quest.idn}\nTime: {quest.date_and_time}\nSender: {quest.sender}\n'
            f'Answered: {quest.answered}\nQuestion:\n{quest.text}\nComments:\n{quest.comments}\n')
    print(quest.idn)
    return text


def print_ans(ans):
    text = (f'id: {ans.idn}\nTime: {ans.date_and_time}\nSender: {ans.sender}\n'
            f'Answer:\n{ans.text}\n')
    return text


def fetch_questions():
    dict_of_questions = {}
    query = CUR.execute('SELECT * FROM questions')
    questions = query.fetchall()
    for quest in questions:
        dict_of_questions.update({quest[0]: Question(idn=quest[0], date_and_time=quest[1], sender=quest[2],
                                                     answered=quest[4], comments=quest[5], text=quest[3])})
    return dict_of_questions


def fetch_answers():
    dict_of_answers = {}
    query = CUR.execute('SELECT * FROM answers')
    answers = query.fetchall()
    for ans in answers:
        dict_of_answers.update({ans[0]: Answer(idn=ans[0], date_and_time=ans[1], sender=ans[2],
                                               text=ans[3])})
    return dict_of_answers


def show_new_questions():
    dict_of_questions = fetch_questions()
    sorted_questions = dict(sorted(dict_of_questions.items()))
    text = ""
    for quest in sorted_questions.values():
        if quest.answered == 'New':
            text += print_quest(quest)
            text += '====================================\n'
    messagebox.showinfo('New questions', text)


def show_answered():
    dict_of_quest = fetch_questions()
    dict_of_ans = fetch_answers()
    text = ""
    sorted_questions = dict(sorted(dict_of_quest.items()))
    for qid, quest in sorted_questions.items():
        if qid in dict_of_ans.keys():
            text += print_quest(quest)
            text += '------------------------------------\n'
            text += print_ans(dict_of_ans[qid])
            text += '====================================\n'
    messagebox.showinfo('Answered questions', text)


def show_all_questions():
    dict_of_questions = fetch_questions()
    sorted_questions = dict(sorted(dict_of_questions.items()))
    text = ""
    for quest in sorted_questions.values():
        text += print_quest(quest)
        text += '====================================\n'
    messagebox.showinfo('All questions', text)


def show_all_answers():
    dict_of_ans = fetch_answers()
    sorted_answers = dict(sorted(dict_of_ans.items()))
    text = ""
    for ans in sorted_answers.values():
        text += print_ans(ans)
        text += '====================================\n'
    messagebox.showinfo('All answers', text)


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
    CONN, CUR = dbconnect()

    window = Tk()
    window.title("messenger")
    window.geometry("600x250")

    row = 0

    lbl_username = Label(text="username:")
    lbl_username.grid(column=0, row=row)

    entry_username = Entry(window, width=10)
    entry_username.grid(column=1, row=row)

    lbl_pwd = Label(text="password:")
    lbl_pwd.grid(column=2, row=row)

    entry_pwd = Entry(window, width=10)
    entry_pwd.grid(column=3, row=row)

    row = 1

    btn_login = Button(window, text="log in", command=login)
    btn_login.grid(column=0, row=row)

    btn_signup = Button(window, text="sign up", command=signup)
    btn_signup.grid(column=1, row=row)

    row = 2

    btn_show_all_questions = Button(window, text="show all questions", command=show_all_questions)
    btn_show_all_questions.grid(column=0, row=row)

    btn_show_all_answers = Button(window, text="show all answers", command=show_all_answers)
    btn_show_all_answers.grid(column=1, row=row)

    btn_show_new_questions = Button(window, text="show new questions", command=show_new_questions)
    btn_show_new_questions.grid(column=2, row=row)

    btn_show_answered = Button(window, text="show answered questions", command=show_answered)
    btn_show_answered.grid(column=3, row=row)

    row = 3

    btn_ask = Button(window, text="new question", command=new_question)
    btn_ask.grid(column=0, row=row)

    btn_answer = Button(window, text="new answer", command=answer_question)
    btn_answer.grid(column=1, row=row)

    row = 4

    lbl_new_text = Label(window, text="Your text:")
    lbl_new_text.grid(column=0, row=row)

    entry_new_text = Entry(window, width=50)
    entry_new_text.grid(column=0, row=row, columnspan=4)

    row = 5

    lbl_qid = Label(window, text="Question id:")
    lbl_qid.grid(column=0, row=row)

    entry_qid = Entry(window, width=50)
    entry_qid.grid(column=0, row=row, columnspan=4)

    window.mainloop()
