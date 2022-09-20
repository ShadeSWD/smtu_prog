import random

def creale_arr(length):
    list_of_int =  []
    for i in range(length):
        list_of_int.append(random.randint(1, 99))
    return list_of_int


def bubble_sort(list_of_int):
    for i in range(len(list_of_int) - 1):
        for j in range(len(list_of_int) - i -1):
            if list_of_int[j] > list_of_int[j + 1]:
                tmp = list_of_int[j]
                list_of_int[j] = list_of_int[j + 1]
                list_of_int[j + 1] = tmp
    return(list_of_int)

if __name__ == "__main__":
    list_of_int = creale_arr(10)
    print(list_of_int)
    list_of_int = bubble_sort(list_of_int)
    print(list_of_int)
    