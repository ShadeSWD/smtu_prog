def check_list(simples, element):
    flag = True
    for i in simples:
        if ((i == element) or (element % i == 0)) and (i != 1):
            flag = False
    return flag


def calculate(number):
    simples = []
    simples.append(1)
    i = 1
    summ = 0
    while len(simples) <= number:
        if check_list(simples, i):
            summ += i ** 2
            simples.append(i)
        i += 1
    print(summ)


if __name__ == "__main__":
    data = int(input('Type a number'))
    calculate(data)
