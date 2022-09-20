from datetime import datetime
import re

class NewQuestion:
    def __init__(self):
        self.id = 'q'
        self.date_and_time = None
        self.text = None
        self.sender = None
        self.answered = False
        self.comments = None
        
    def collect_data(self):
        self.date_and_time = datetime.now()
        self.sender = input('Your name:\n')
        self.text = input('Your question:\n')
        time_list = re.findall('\d', str(self.date_and_time))
        for i in time_list:
            self.id += i
        self.id += self.sender[0].lower()
    
    def output_data(self):  
        #  filename = self.id + '.txt'
        output = (f'$new_question\n$id={self.id}$time={self.date_and_time}$sender={self.sender}$answered={self.answered}$comments={self.comments}$question={self.text}\n')
        with open("questions.txt", "a") as f:
            f.write(output)
        
    def run_node(self):
        self.collect_data()
        self.output_data()
    
if __name__ == "__main__":
    new_question = NewQuestion()
    new_question.run_node()
