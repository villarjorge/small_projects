import numpy as np
import datetime as dt
from colorama import init, Fore, Back, Style

rng = np.random.default_rng()
# Necesary for the module to work in windows
init()

def random_date():
    """Returns a random date as a tuple (year, month, day) with all days equaly likely"""
    rand_year, rand_month = rng.integers((0, 1), (3000, 12))
    # Leap year
    if rand_year % 4 == 0 and rand_month == 2:
        rand_day = rng.integers(1, 29)
        return (rand_year, rand_month, rand_day)
    # Not leap year, february
    if rand_month == 2:
        rand_day = rng.integers(1, 28)
        return (rand_year, rand_month, rand_day)
    # Months with 30 days
    if rand_month in (4, 6, 9, 11):
        rand_day = rng.integers(1, 30)
        return (rand_year, rand_month, rand_day)
    # Else
    rand_day = rng.integers(1, 31)
    return (rand_year, rand_month, rand_day)

def look_points():
    """Looks up the wins and losses of the player"""
    with open("score.txt", "r") as score:
        # score.txt consist of two numbers, the recorded wins and the recorded losses.
        # A win is getting the day right and a loss is the opposite
        wins, losses = score.read().split(",")
        return (int(wins), int(losses))

def update_points(is_win: bool):
    """Updates the points depending if the condition is win (True) or loss (false)"""
    wins, losses = look_points()
    # Update values
    if is_win:
        wins += 1
    else:
        losses += 1
    with open("score.txt", "w") as score:
        # score.txt consist of two numbers, the recorded wins and the recorded losses.
        # A win is getting the day right and a loss is the opposite
        score.write(f"{wins},{losses}")

def create_date():
    """Creates the random date"""
    # I know that this is not the best way
    #rand_year, rand_month, rand_day = rng.integers((0, 1, 1), (3000, 12, 31))# rng.integers(0, 3000), rng.integers(1, 12), rng.integers(1, 31)
    
    rand_year, rand_month, rand_day = random_date()

    date_object = dt.date(rand_year, rand_month, rand_day)
    #print(date_object.weekday())
    return rand_year, rand_month, rand_day, date_object

def get_answer(rand_year, rand_month, rand_day, date_object):
    """Asks the question and handles the response"""
    print(f"Date: {date_object} or {rand_day} of {months_num_to_name[rand_month]} of {rand_year}")
    # If you want to cheat you can uncomment the line below and coment the other print, this will the answer in black next to the question
    #print(f"{Back.BLACK}What day of the week was that, by name?{Fore.BLACK}{date_object.weekday()+1}{Style.RESET_ALL} ")
    print(f"What day of the week was that, by name?")
    answer = input().capitalize()
    if answer == "Stop" or answer == "Exit":
        print("Program stopped")
        wins, losses = look_points()
        print(f"{Fore.GREEN}Wins: {wins}, {Fore.RED}Losses: {losses}{Style.RESET_ALL}")
        exit()
    try:
        days_name_to_num[answer]
    except KeyError:
        print("I do not understand that. A spelling error? Input stop or the day of the week you think it is in lower case")
        get_answer(rand_year, rand_month, rand_day, date_object)
    else:
        if days_name_to_num[answer] == (date_object.weekday()+1) % 7:
            doomsday = (dt.date(rand_year, 4, 4).weekday() + 1) % 7
            print(f"{Fore.GREEN}Correct! The doomsday of that year was a {days_num_to_name[doomsday]} ({doomsday}) so {date_object} was a {answer}{Style.RESET_ALL}")
            update_points(is_win=True)
            wins, losses = look_points()
            print(f"{Fore.GREEN}Wins: {wins}, {Fore.RED}Losses: {losses}{Style.RESET_ALL}")
            year, month, day, date_obj = create_date()
            get_answer(year, month, day, date_obj)
        else:
            print(f"{Fore.RED}Incorrect{Style.RESET_ALL}")
            update_points(is_win=False)
            get_answer(rand_year, rand_month, rand_day, date_object)

if __name__ == "__main__":
    print("To exit the program, write stop or exit")
    months_num_to_name = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June"	, 7: "July"	, 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    days_num_to_name = {0: "Sunday", 1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday"}
    days_name_to_num = {"Sunday":0, "Monday":1, "Tuesday":2, "Wednesday":3, "Thursday":4, "Friday":5, "Saturday":6}
    year, month, day, date_obj = create_date()
    get_answer(year, month, day, date_obj)