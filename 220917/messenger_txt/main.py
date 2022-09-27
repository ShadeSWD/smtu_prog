import send_from_plant
import read_questions


class MainNode:
    def __init__(self):
        self.list_of_questions = []

    def read_questions(self):
        self.list_of_questions = read_questions.read()

    def show_questions(self):
        for question in self.list_of_questions:
            print(f"Question {question.idn}:\nTime: {question.date_and_time}\nSender: {question.sender}\nQuestion:\n{question.text}\n")
            if question.comments != "None":
                print("Comments:\n{question.comments}\n")


if __name__ == "__main__":
    main = MainNode()
    sender = send_from_plant.NewQuestion()
    while 1:
        main.read_questions()
        choice = int(input('Press 0 to exit, 1 to read, 2 to ask:\n'))
        if choice == 0:
            break
        if choice == 1:
            main.show_questions()
        if choice == 2:
            sender.run_node()
