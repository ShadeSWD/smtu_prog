import random
import re

LENGTH = 4


def get_try():
    flag = False
    while not flag:
        while 1:
            new_try = input(f"Type an int of {LENGTH} digits \n")
            if len(new_try) == LENGTH:
                if re.fullmatch(r'\d+', new_try) is not None:
                    break
                else:
                    print("Incorrect symbols")
            else:
                print("Incorrect length")
        match = 0
        i = 0
        while i < LENGTH:
            if new_try.find(new_try[i], i + 1) != -1:
                match += 1
            i += 1
        if match == 0:
            flag = True
        else:
            print('digits must be different')
    return new_try


def spawn_number():
    number = str(random.randint(0, 9))
    while len(number) < LENGTH:
        while 1:
            bit = str(random.randint(0, 9))
            if number.find(bit) == -1:
                number += bit
                break
    return number


def play_game(number):
    attempt = 1
    while 1:
        print(f"Attempt: {attempt}")
        new_try = get_try()
        bulls = 0
        cows = 0
        i = 0
        while i < LENGTH:
            if number.find(new_try[i]) != -1:
                if number[i] == new_try[i]:
                    bulls += 1
                else:
                    cows += 1
            i += 1
        attempt += 1
        print(f"Bulls: {bulls}, cows: {cows} \n")
        if bulls == LENGTH:
            print("Congratulations!")
            break


if __name__ == "__main__":
    game_number = spawn_number()
    print(game_number)
    play_game(game_number)
