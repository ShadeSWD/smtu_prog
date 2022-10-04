import xml.etree.ElementTree as ElT
from datetime import datetime
import re
from collections import namedtuple
import os.path

Question = namedtuple('Question', 'idn date_and_time text sender answered comments')
Answer = namedtuple('Answer', 'idn date_and_time text sender')

bundle = ElT.Element('bundle')
question = ElT.SubElement(bundle, 'Question')
idn = ElT.SubElement(question, 'Idn')
date_time = ElT.SubElement(question, 'Time')
text = ElT.SubElement(question, 'Text')
sender = ElT.SubElement(question, 'Sender')
status = ElT.SubElement(question, 'Status')
comments = ElT.SubElement(question, 'Comments')

bundle = ElT.Element('bundle')
user = ElT.SubElement(bundle, 'User')
name = ElT.SubElement(user, 'Name')
password = ElT.SubElement(user, 'Password')

FILE_OF_QUESTIONS = 'questions.xml'
FILE_OF_ANSWERS = 'answers.xml'
FILE_OF_USERS = 'users.xml'
HEAD = '<?xml version="1.0" encoding="utf-8"?>\n'


def login():
    n_name = input('Name:\n')
    n_password = input('Password:\n')
    return n_name


def signup():
    dict_of_users = {}
    if os.path.exists(FILE_OF_USERS):
        dict_of_users = collect_old_users()

    n_name = input('Name:\n')
    while 1:
        n_password = input('Password:\n')
        rpt = input('Repeat password:\n')
        if n_password == rpt:
            break
        else:
            print('Passwords are not the same!\n')
    dict_of_users.update({n_name: n_password})
    print(dict_of_users)
    return n_name


def collect_old_users():
    dict_of_us = {}
    tree = ElT.parse(FILE_OF_USERS)
    root = tree.getroot()
    for child in root:
        n_user = ''
        n_password = None
        for element in child:
            if element.tag == 'Name':
                n_user = element.text
            if element.tag == 'Password':
                n_password = element.text
        dict_of_us.update({n_user: n_password})
    return dict_of_us


def collect_old_questions():
    list_of_quest = []
    tree = ElT.parse(FILE_OF_QUESTIONS)
    root = tree.getroot()
    for child in root:
        qid = ''
        n_answered = None
        n_comments = ''
        date_and_time = ''
        n_sender = ''
        n_text = ''
        for element in child:
            if element.tag == 'Idn':
                qid = element.text
            if element.tag == 'Time':
                date_and_time = element.text
            if element.tag == 'Sender':
                n_sender = element.text
            if element.tag == 'Status':
                n_answered = element.text
            if element.tag == 'Comments':
                n_comments = element.text
            if element.tag == 'Text':
                n_text = element.text
        list_of_quest.append(Question(idn=qid, date_and_time=str(date_and_time), sender=n_sender,
                                      answered=n_answered, comments=n_comments, text=n_text))
    return list_of_quest


def new_question(usr):
    qid = ''
    answered = None
    date_and_time = datetime.now()
    n_sender = usr
    n_text = input('Your question:\n')
    time_list = re.findall('\d', str(date_and_time))
    for i in time_list:
        qid += i
    qid += n_sender[0].lower()

    return Question(idn=qid, date_and_time=str(date_and_time), sender=n_sender,
                    answered=answered, comments=comments, text=n_text)


def form_xml_questions(quest):
    idn.text = quest.idn
    date_time.text = quest.date_and_time
    text.text = quest.text
    sender.text = quest.sender
    status.text = quest.answered
    comments.text = quest.comments

    dat = ElT.tostring(question, encoding='unicode')

    return dat


def form_xml_users(n_name, n_password):
    name.text = n_name
    password.text = n_password
    dat = ElT.tostring(user, encoding='unicode')

    return dat


def rewrite_questions(list_of_quest):
    q_file = open(FILE_OF_QUESTIONS, 'w')
    dat = HEAD
    dat += '<bundle>\n'
    for quest in list_of_quest:
        dat = dat + '  ' + form_xml_questions(quest) + '\n'
    dat += '</bundle>\n'
    q_file.write(dat)
    q_file.close()


def rewrite_users(dict_of_users):
    q_file = open(FILE_OF_USERS, 'w')
    dat = HEAD
    dat += '<bundle>\n'
    for usr in dict_of_users:
        dat = dat + '  ' + form_xml_users(usr, 1) + '\n'
    dat += '</bundle>\n'
    q_file.write(dat)
    q_file.close()


def show_questions(list_of_quest):
    for quest in list_of_quest:
        print(f'id: {quest.idn}\nTime: {quest.date_and_time}\nSender: {quest.sender}\n'
              f'Answered: {quest.answered}\nQuestion:\n{quest.text}\nComments:\n{quest.comments}\n')


def answer_question(qid, usr):
    time = datetime.now()


if __name__ == '__main__':
    ch = int(input('Press 0 to login, 1 to sign up:\n'))
    user = None
    while not user:
        if ch == 0:
            user = login()
        if ch == 1:
            user = signup()
    list_of_questions = []
    if os.path.exists(FILE_OF_QUESTIONS):
        list_of_questions = collect_old_questions()
    while 1:
        choice = int(input('Press 0 to exit, 1 to read, 2 to ask, 3 to answer:\n'))
        if choice == 0:
            break
        if choice == 1:
            show_questions(list_of_questions)
        if choice == 2:
            data = new_question(user)
            list_of_questions.append(data)
        if choice == 3:
            answer_id = input('Question ID:\n')
            answer_question(answer_id, user)
        rewrite_questions(list_of_questions)
