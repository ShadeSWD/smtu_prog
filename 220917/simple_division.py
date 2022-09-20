def check_list(simples, element):
    flag = True
    for i in simples:
        if ((i == element) or (element % i == 0)) and (i != 1):
            flag = False
    return flag


def check_number(number):
    simples = []
    simples.append(1)
    for i in range(1, (number // 2) + 1):
        flag = check_list(simples, i)
        if ((number % i == 0) and flag) and (i != 1):
            simples.append(i)
    print(simples)


if __name__ == "__main__":
    num = int(input('Type a number'))
    check_number(num)
