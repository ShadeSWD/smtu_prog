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

answer = ElT.SubElement(bundle, 'Answer')
a_idn = ElT.SubElement(answer, 'Idn')
a_date_time = ElT.SubElement(answer, 'Time')
a_text = ElT.SubElement(answer, 'Text')
a_sender = ElT.SubElement(answer, 'Sender')

bundle = ElT.Element('bundle')
user = ElT.SubElement(bundle, 'User')
name = ElT.SubElement(user, 'Name')
password = ElT.SubElement(user, 'Password')

FILE_OF_QUESTIONS = 'questions.xml'
FILE_OF_ANSWERS = 'answers.xml'
FILE_OF_USERS = 'users.xml'
HEAD = '<?xml version="1.0" encoding="utf-8"?>\n'


def login():
    dict_of_us = collect_old_users()
    while 1:
        n_name = input('Name:\n')
        try:
            u_pwd = dict_of_us[n_name]
            while 1:
                n_password = input('Password:\n')
                if n_password == u_pwd:
                    break
                else:
                    print('Incorrect password')
            break
        except KeyError:
            print('Username is incorrect')
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
    rewrite_users(dict_of_users)
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
    dict_of_quest = {}
    tree = ElT.parse(FILE_OF_QUESTIONS)
    root = tree.getroot()
    for child in root:
        qid = ''
        n_answered = ''
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
        dict_of_quest.update({qid: Question(idn=qid, date_and_time=str(date_and_time), sender=n_sender,
                                            answered=n_answered, comments=n_comments, text=n_text)})
    return dict_of_quest


def collect_old_answers():
    dict_of_ans = {}
    tree = ElT.parse(FILE_OF_ANSWERS)
    root = tree.getroot()
    for child in root:
        qid = ''
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
            if element.tag == 'Text':
                n_text = element.text
        dict_of_ans.update({qid: Answer(idn=qid, date_and_time=str(date_and_time), sender=n_sender,
                                        text=n_text)})
    return dict_of_ans


def answer_question(qid, usr):
    n_time = datetime.now()
    n_text = input('Answer:\n')

    return {qid: Answer(idn=qid, date_and_time=str(n_time), sender=usr, text=n_text)}


def new_question(usr):
    qid = ''
    answered = 'New'
    date_and_time = datetime.now()
    n_sender = usr
    n_text = input('Your question:\n')
    time_list = re.findall('\d', str(date_and_time))
    for i in time_list:
        qid += i
    qid += n_sender[0].lower()

    return {qid: Question(idn=qid, date_and_time=str(date_and_time), sender=n_sender,
                          answered=answered, comments=comments, text=n_text)}


def form_xml_questions(quest):
    idn.text = quest.idn
    date_time.text = quest.date_and_time
    text.text = quest.text
    sender.text = quest.sender
    status.text = quest.answered
    comments.text = quest.comments

    dat = ElT.tostring(question, encoding='unicode')

    return dat


def form_xml_answers(ans):
    a_idn.text = ans.idn
    a_date_time.text = ans.date_and_time
    a_text.text = ans.text
    a_sender.text = ans.sender

    dat = ElT.tostring(answer, encoding='unicode')

    return dat


def form_xml_users(n_name, n_password):
    name.text = n_name
    password.text = n_password
    dat = ElT.tostring(user, encoding='unicode')

    return dat


def rewrite_answers(dict_of_ans):
    q_file = open(FILE_OF_ANSWERS, 'w')
    dat = HEAD
    dat += '<bundle>\n'
    for ans in dict_of_ans.values():
        dat = dat + '  ' + form_xml_answers(ans) + '\n'
    dat += '</bundle>\n'
    q_file.write(dat)
    q_file.close()


def rewrite_questions(dict_of_quest):
    q_file = open(FILE_OF_QUESTIONS, 'w')
    dat = HEAD
    dat += '<bundle>\n'
    for quest in dict_of_quest.values():
        dat = dat + '  ' + form_xml_questions(quest) + '\n'
    dat += '</bundle>\n'
    q_file.write(dat)
    q_file.close()


def rewrite_users(dict_of_users):
    q_file = open(FILE_OF_USERS, 'w')
    dat = HEAD
    dat += '<bundle>\n'
    for usr, pwd in dict_of_users.items():
        dat = dat + '  ' + form_xml_users(usr, pwd) + '\n'
    dat += '</bundle>\n'
    q_file.write(dat)
    q_file.close()


def print_quest(quest):
    print(f'id: {quest.idn}\nTime: {quest.date_and_time}\nSender: {quest.sender}\n'
          f'Answered: {quest.answered}\nQuestion:\n{quest.text}\nComments:\n{quest.comments}\n')


def print_ans(ans):
    print(f'id: {ans.idn}\nTime: {ans.date_and_time}\nSender: {ans.sender}\n'
          f'Answer:\n{ans.text}\n')


def show_new_questions(dict_of_quest):
    sorted_questions = dict(sorted(dict_of_quest.items()))
    for quest in sorted_questions.values():
        if quest.answered == 'New':
            print_quest(quest)
            print('====================================\n')


def show_answered(dict_of_quest, dict_of_ans):
    sorted_questions = dict(sorted(dict_of_quest.items()))
    for qid, quest in sorted_questions.items():
        if qid in dict_of_ans.keys():
            print_quest(quest)
            print('------------------------------------\n')
            print_ans(dict_of_ans[qid])
            print('====================================\n')


def show_all_questions(dict_of_quest):
    sorted_questions = dict(sorted(dict_of_quest.items()))
    for quest in sorted_questions.values():
        print_quest(quest)
        print('====================================\n')


def show_all_answers(dict_of_ans):
    sorted_answers = dict(sorted(dict_of_ans.items()))
    for ans in sorted_answers.values():
        print_ans(ans)
        print('====================================\n')


if __name__ == '__main__':
    ch = int(input('Press 0 to login, 1 to sign up:\n'))
    c_user = None
    while not c_user:
        if ch == 0:
            c_user = login()
        if ch == 1:
            c_user = signup()
    dict_of_questions = {}
    if os.path.exists(FILE_OF_QUESTIONS):
        dict_of_questions = collect_old_questions()
    dict_of_answers = {}
    if os.path.exists(FILE_OF_ANSWERS):
        dict_of_answers = collect_old_answers()
    while 1:
        choice = int(input('Press 0 to exit, 1 to read, 2 to ask, 3 to answer:\n'))
        if choice == 0:
            break
        if choice == 1:
            ch1 = int(input('Press 0 to exit, 1: all questions, 2: all answers, 3: new, 4: answered\n'))
            if ch1 == 0:
                pass
            if ch1 == 1:
                show_all_questions(dict_of_questions)
            if ch1 == 2:
                show_all_answers(dict_of_answers)
            if ch1 == 3:
                show_new_questions(dict_of_questions)
            if ch1 == 4:
                show_answered(dict_of_questions, dict_of_answers)
        if choice == 2:
            data = new_question(c_user)
            dict_of_questions.update(data)
        if choice == 3:
            while 1:
                answer_id = input('Question ID:\n')
                if answer_id in dict_of_questions.keys():
                    dict_of_questions.update({answer_id: Question(idn=dict_of_questions[answer_id].idn,
                                                                  date_and_time=dict_of_questions[
                                                                      answer_id].date_and_time,
                                                                  text=dict_of_questions[answer_id].text,
                                                                  sender=dict_of_questions[answer_id].sender,
                                                                  comments=dict_of_questions[answer_id].comments,
                                                                  answered='Answered')})
                    dict_of_answers.update(answer_question(answer_id, c_user))
                    break
                else:
                    print('Incorrect question id')
                break
        rewrite_questions(dict_of_questions)
        rewrite_answers(dict_of_answers)
