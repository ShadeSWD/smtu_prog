from collections import namedtuple
import re

Element = namedtuple('Element', 'num quant')
list_of_data = []


def check_integer(dat):
    if re.fullmatch('\d+', dat):
        return True
    else:
        return False


def input_data():
    flag = False
    dat = None
    while not flag:
        dat = input()
        flag = check_integer(dat)
    return dat


def process_data(dat):
    print(len(dat))
    i = 0
    while i < (len(dat)):
        current_number = dat[i]
        quantity = 1
        i += 1
        try:
            while current_number == dat[i]:
                i += 1
                quantity += 1
            list_of_data.append(Element(current_number, quantity))
        except IndexError:
            list_of_data.append(Element(current_number, quantity))
    return list_of_data


def output_data(dat):
    out = ''
    for element in dat:
        out += str(element.num) + ',' + str(element.quant) + ' '
    print(out)


if __name__ == "__main__":
    data = input_data()
    data = process_data(data)
    output_data(data)
