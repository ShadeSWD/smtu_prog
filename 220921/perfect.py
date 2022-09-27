import re


def check_list(simples, element):
    flag = True
    for i in simples:
        if ((i == element) or (element % i == 0)) and (i != 1):
            flag = False
    return flag


def get_number():
    while 1:
        data = input(f"Type number:\n")
        if re.fullmatch(r'\d+', data) is not None:
            break
        else:
            print("Incorrect symbols")
    return int(data)


def check_number(data):
    simples = [1]
    for i in range(1, (data // 2) + 1):
        if (number % i == 0) and (i != 1):
            simples.append(i)
    if sum(simples) == data:
        print('True')
    else:
        print('False')


if __name__ == "__main__":
    number = get_number()
    check_number(number)
