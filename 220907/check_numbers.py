from collections import namedtuple
import re

Element = namedtuple('Element', 'num quant')
list_of_data = []

def check_integer(data)
    if re.fullmatch('d+', data)
        return True
    else
        return False

def input_data()
    flag = False
    while flag == False
        data = input()
        flag = check_integer(data)
    return data

def process_data(data)
    print(len(data))
    i = 0
    while i  (len(data))
        current_number = data[i]
        quantity = 1
        i += 1
        try
            while current_number == data[i]
                i += 1
                quantity += 1
            list_of_data.append(Element(current_number, quantity))
        except IndexError
            list_of_data.append(Element(current_number, quantity))
    return list_of_data
            
def output_data(data)
    out = ''
    for element in data
        out += str(element.num) + ',' + str(element.quant) + ' '
    print(out)

if __name__ == __main__
    data = input_data()
    data = process_data(data)
    output_data(data)