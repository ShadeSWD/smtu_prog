import random

def creale_arr(length):
    list_of_int =  []
    for i in range(length):
        list_of_int.append(random.randint(-10, 10))
    return list_of_int
    
def custom_arr():
    custom = [-3, 7, 12, 13, 12]
    return custom
    
def bubble_sort(list_of_int):
    for i in range(len(list_of_int) - 1):
        for j in range(len(list_of_int) - i -1):
            if list_of_int[j] > list_of_int[j + 1]:
                tmp = list_of_int[j]
                list_of_int[j] = list_of_int[j + 1]
                list_of_int[j + 1] = tmp
    return(list_of_int)
    
def check_list(list_of_int, summ):
    flag = False
    for i in range(len(list_of_int)):
        for j in range(i + 1, len(list_of_int)):
            if list_of_int[i] + list_of_int[j] == summ:
                print(list_of_int[i], list_of_int[j])
                flag = True
                break
        if flag == True:
            break
    if flag == False:
        print(-1)

if __name__ == "__main__":
    list_of_int = creale_arr(5)
    # list_of_int = custom_arr()
    list_of_int = bubble_sort(list_of_int)
    print(list_of_int)
    summ = int(input())
    check_list(list_of_int, summ)
    