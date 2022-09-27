import send_from_plant
import dump_questions
import read_questions
import xml.etree.ElementTree as ElT


question = ElT.Element('Question')
idn = ElT.SubElement(question, 'Idn')
date_time = ElT.SubElement(question, 'Time')
text = ElT.SubElement(question, 'Text')
sender = ElT.SubElement(question, 'Sender')
status = ElT.SubElement(question, 'Status')
comments = ElT.SubElement(question, 'Comments')


class MainNode:
    def __init__(self):
        self.list_of_questions = []

    def read_questions(self):
        self.list_of_questions = read_questions.read()


if __name__ == "__main__":
    main = MainNode()
    sender = send_from_plant.NewQuestion()
    while 1:
        main.read_questions()
        choice = int(input('Press 0 to exit, 1 to read, 2 to ask:\n'))
        if choice == 0:
            break
        if choice == 1:
            read_questions.read()
        if choice == 2:
            sender.run_node()
