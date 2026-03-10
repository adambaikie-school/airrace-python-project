# Imports
import os
import time
import random

# Variables

game_phase = 1
progress = 0

# Constant Variables


# Functions

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def problem_game(gamephase):
    if gamephase == 1:
        print("You have just taken off, you notice the landing gear did not retract. \n")
        time.sleep(3)
        print("What do you do? \n")
        print("1. Ignore it, and hope it doesn't cause any problems. \n")
        print("2. Try to retract it manually. \n")
        print("3. Try to fix it with the tools in the cockpit. \n")
        try:
            answer = input("What do you do? 1,2,3: ")
        except ValueError:
            print("Invalid input. Please enter a number.")
            return(1)
        if answer not in ("1", "2", "3"):
            print("Invalid input. Please enter a number.")
            return(1)
        if answer == "1":
            print("You ignore the problem, and continue flying. \n")
            time.sleep(3)
            clear_console()
            return(1)
        elif answer == "2":
            print("You try to retract the landing gear manually, but it doesn't work. \n")
            time.sleep(3)
            clear_console()
            return(1)
        elif answer == "3":
            print("You try to fix the problem with the tools in the cockpit, and the gear retracts. \n")
            time.sleep(3)
            clear_console()
            return(0)
    elif gamephase == 2:
        random_number = random.randint(1, 5)
        if random_number == 1:
            print("You encounter a storm, and your plane is damaged. \n")
            time.sleep(3)
            clear_console()
            return(1)
        elif random_number == 2:
            print("You encounter turbulence, and your plane is damaged. \n")
            time.sleep(3)
            clear_console()
            return(1)
        elif random_number == 3:
            print("You encounter a flock of birds, and your plane is damaged. \n")
            time.sleep(3)
            clear_console()
            return(1)
        elif random_number == 4:
            print("You encounter a mountain, and your plane is damaged. \n")
            time.sleep(3)
            clear_console()
            return(1)
        elif random_number == 5:
            print("You encounter a clear sky. Your Plane is not damaged. \n")
            time.sleep(3)
            clear_console()
            return(0)

# loops
while True:
    print("Welcome to Air Race! \n")
    print("The aim of this game, is to race across the world, the fastest way possible! \n")
    print("However, along the way you may discover problems and find ways to fix them.\n")
    answer = input("Are you ready to race? Yes/No: ")
    if answer not in ("yes", "y", "Yes", "Y"):
        clear_console()
        print("Okay! Hope your ready next time!")
        time.sleep(3)
        continue
    print("Here are the controls:\n")
    print("You will be using the numbers 1,2,3,4,5 to choose your path.")
    print("Use 'A' and 'D' when prompted!")
    time.sleep(3)
    clear_console()
    print("You are in the cockpit of your plane, you are ready to take off! \n")
    time.sleep(3)
    clear_console()
    problem_value = problem_game(game_phase)
    if problem_value == 1:
        print("Your plane is damaged, and you have to land. \n")
        time.sleep(3)
        clear_console()
    elif problem_value == 0:
        print("You continue flying, and you are doing well! \n")
        time.sleep(3)
        progress += 5
        print(f"You have now traveled {progress}% of the world!\n")
        clear_console()
    




