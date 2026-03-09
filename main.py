# Imports
import os
import time


# Variables


# Constant Variables


# Functions

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


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




