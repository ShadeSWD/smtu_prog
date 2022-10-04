from collections import namedtuple
import template

Question = namedtuple('Question', 'idn date_and_time text sender answered comments')


def dump(inp):
    # data = template.head
    data = ""
    if inp.idn is not None:
        data = data + template.xml_builder(n_idn=inp.idn, n_date_and_time=inp.date_and_time, n_sender=inp.sender,
                                           n_answered=inp.answered, n_comments=inp.comments, n_text=inp.text) + "\n"
    mf = open('questions.xml', 'a')
    mf.write(data)
    mf.close()


