import random


def say_hello():
    print('This is a game, press Enter to start')
    input()
    
    
def check_integer(number):
    try:
        if str(int(number)) == number:
            return True
        else:
            print('Numbers must be integer')
            return False
    except ValueError:
        print('Numbers must be integer')
        return False
        
        
def input_number(text):
    flag = False
    while flag == False:
        number = input(text)
        flag = check_integer(number)
    return int(number)
    
    
def input_lower_limit():
    lower_limit = input_number('Enter a minimum limit')
    return lower_limit
    
    
def input_upper_limit(lower_limit):
    upper_limit = input_number('Enter a maximum limit')
    while upper_limit <= lower_limit:
        print('Upper limit is under lower limit')
        upper_limit = input_number('Enter a maximum limit')
    return upper_limit
    
    
def input_game_number(lower_limit, upper_limit):
    number = input_number('Type your number')
    while (number < lower_limit) or (number > upper_limit):
        print('Your number is out of range')
        number = input_number('Type your number')
    return number
    
    
def check_number(number, game_number):
    finish_flag = False
    if number == game_number:
        print('You won .-)')
        finish_flag = True
    elif number > game_number:
        print('You typed a bigger number')
    elif number < game_number:
        print('You typed a smaller number')
    return finish_flag
    

def play_game():
    lower_limit = input_lower_limit()
    upper_limit = input_upper_limit(lower_limit)
    game_number = random.randint(lower_limit, upper_limit)
    print('Debug: ', game_number)
    max_attempts = input_number('Enter maximum attempts')
    current_attempt = 1
    while current_attempt <= max_attempts:
        print("Attempt: ", current_attempt)
        number = input_game_number(lower_limit, upper_limit)
        finish_flag = check_number(number, game_number)
        if finish_flag:
            break
        current_attempt += 1
    print('Game over')
        

if __name__ == "__main__":
    say_hello()
    play_game()