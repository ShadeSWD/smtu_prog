from collections import namedtuple


Question = namedtuple('Question', 'idn date_and_time text sender answered comments')


def read():
    list_of_questions = []
    with open("questions.txt", "r") as f:
        for line in f:
            idn = None
            date_and_time = None
            text = None
            sender = None
            answered = False
            comments = None
            spl = line[0: -1].split('$')
            for bit in spl:
                try:
                    bit = bit.split("=")
                    if bit[0] == "id":
                        idn = bit[1]
                    if bit[0] == "time":
                        date_and_time = bit[1]
                    if bit[0] == "sender":
                        sender = bit[1]
                    if bit[0] == "answered":
                        answered = bit[1]
                    if bit[0] == "comments":
                        comments = bit[1]
                    if bit[0] == "text":
                        text = bit[1]
                except IndexError:
                    pass
            if idn is not None:
                list_of_questions.append(Question(idn=idn, date_and_time=date_and_time, sender=sender,
                                                  answered=answered, comments=comments, text=text))
    return list_of_questions

