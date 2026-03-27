# Imports

import os
import random
import time

# Constants and Data
WORLD_PROGRESS = 100
LEG_PROGRESS = 10
TRAVEL_DAYS_PER_LEG = 2
SEARCH_CHOICES = 3

# Each repair problem links a type of damage to the item needed to fix it.
REPAIR_PROBLEMS = {
    "landing_gear": {
        "problem": "Your landing gear jams and will not retract.",
        "required_item": "Tool Kit",
        "repair_text": "You free the landing gear with the tool kit and it locks into place.",
    },
    "propeller": {
        "problem": "A bird strike cracks your propeller.",
        "required_item": "Propeller",
        "repair_text": "You bolt on the spare propeller and the engine runs smoothly again.",
    },
    "wing": {
        "problem": "A storm tears a hole in your wing fabric.",
        "required_item": "Wing Patch",
        "repair_text": "You patch the wing and the plane is ready to fly again.",
    },
    "fuel_line": {
        "problem": "Heavy turbulence splits your fuel line.",
        "required_item": "Fuel Hose",
        "repair_text": "You replace the fuel hose and stop the leak.",
    },
    "engine": {
        "problem": "Dust clogs the engine and it starts coughing badly.",
        "required_item": "Spark Plug",
        "repair_text": "You fit the new spark plug and the engine settles down.",
    },
}

# Items that can appear while searching for plane parts.
SEARCH_ITEM_POOL = [
    "Tool Kit",
    "Propeller",
    "Wing Patch",
    "Fuel Hose",
    "Spark Plug",
    "Map",
    "Key",
    "Seat",
    "Fuel Can",
    "Rope",
    "Compass",
    "Bones",
]

# Takeoff choices decide whether the player causes a landing gear problem.
TAKEOFF_CHOICES = {
    1: {
        "message": "You ignore the warning light and keep climbing.",
        "damage_key": "landing_gear",
    },
    2: {
        "message": "You pull the manual lever, but the gear still sticks.",
        "damage_key": "landing_gear",
    },
    3: {
        "message": "You follow the checklist, reset the system, and the gear retracts cleanly.",
        "damage_key": None,
    },
}

# Random flight events can either damage the plane or let the player continue safely.
AIR_EVENTS = [
    {
        "message": "A flock of birds dives into your flight path.",
        "damage_key": "propeller",
    },
    {
        "message": "A tropical storm batters the plane over the ocean.",
        "damage_key": "wing",
    },
    {
        "message": "Violent turbulence shakes the engine bay.",
        "damage_key": "fuel_line",
    },
    {
        "message": "Dust from a desert runway gets sucked into the engine.",
        "damage_key": "engine",
    },
    {
        "message": "You catch a strong tailwind and the sky stays clear.",
        "damage_key": None,
    },
    {
        "message": "The weather stays calm and the plane handles perfectly.",
        "damage_key": None,
    },
]

# Functions


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def pause(seconds):
    time.sleep(seconds)


def pause_and_clear(seconds=2):
    pause(seconds)
    clear_console()


def prompt_number(prompt, valid_choices):
    # Keep asking until the player enters one of the allowed numbers.
    while True:
        try:
            choice = int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice in valid_choices:
            return choice

        print(f"Invalid input. Please choose from {sorted(valid_choices)}.")


def prompt_yes_no(prompt):
    return input(prompt).strip().lower() in {"yes", "y"}


def format_inventory(inventory):
    if not inventory:
        return "Empty"
    return ", ".join(inventory)


def show_status(day, progress, inventory):
    print(f"Day: {day}")
    print(f"Trip progress: {progress}% / {WORLD_PROGRESS}%")
    print(f"Inventory: {format_inventory(inventory)}\n")
    time.sleep(7)


def show_intro():
    print("Welcome to Air Race!\n")
    print("Your goal is to fly around the world as fast as you can.\n")
    print("Each successful flight leg moves you forward, but damage can force you to land and repair the plane.\n")
    print("If you cannot find the right repair item, you wait until the next day and search again.\n")

    if not prompt_yes_no("Are you ready to race? Yes/No: "):
        clear_console()
        print("Okay! Hope you're ready next time!")
        pause(3)
        return False

    clear_console()
    print("Controls:\n")
    print("Use numbers 1, 2, and 3 when choosing what to do.")
    print("Each flight leg adds progress, and the day counter keeps moving.\n")
    pause_and_clear(15)
    return True


def show_takeoff_scene(day, progress):
    print(f"Day {day}")
    print(f"You are preparing for the next leg of the trip. Current progress: {progress}%.\n")
    pause_and_clear()


def handle_takeoff_problem():
    print("Just after takeoff, a warning light shows the landing gear has not retracted.\n")
    print("1. Ignore it and hope it settles down.")
    print("2. Pull the manual lever harder.")
    print("3. Follow the emergency checklist.\n")

    choice = prompt_number("What do you do? 1, 2, 3: ", set(TAKEOFF_CHOICES))
    outcome = TAKEOFF_CHOICES[choice]

    print(f"\n{outcome['message']}\n")
    pause_and_clear()
    return outcome["damage_key"]


def handle_air_event():
    event = random.choice(AIR_EVENTS)
    print(f"{event['message']}\n")
    pause_and_clear()
    return event["damage_key"]


def choose_flight_problem():
    # Sometimes the danger happens during takeoff, otherwise it happens mid-flight.
    if random.random() < 0.1:
        return handle_takeoff_problem()
    return handle_air_event()


def get_search_options(required_item):
    # The correct repair item only appears sometimes, which can push repairs into the next day.
    other_items = [item for item in SEARCH_ITEM_POOL if item != required_item]

    if random.random() < 0.5:
        options = [required_item] + random.sample(other_items, SEARCH_CHOICES - 1)
    else:
        options = random.sample(other_items, SEARCH_CHOICES)

    random.shuffle(options)
    return options


def search_for_repair_item(problem_data, inventory, day):
    required_item = problem_data["required_item"]

    while True:
        clear_console()
        print(f"Day {day}")
        print(f"{problem_data['problem']}\n")
        print(f"You need a {required_item} to repair the plane.\n")

        search_options = get_search_options(required_item)
        print("You search nearby and find:\n")
        for index, item in enumerate(search_options, start=1):
            print(f"{index}. {item}")
        print()

        choice = prompt_number("Which item do you keep? 1, 2, 3: ", {1, 2, 3})
        saved_item = search_options[choice - 1]
        inventory.append(saved_item)

        print(f"\nYou save the {saved_item}.")

        if saved_item == required_item:
            # Found the required item! Now play a mini-game to use it.
            inventory.remove(required_item)
            result_day = attempt_repair_with_game(problem_data, day)
            
            # If repair succeeded, we're done
            if result_day is not None:
                return result_day
            
            # If repair failed (result_day is None), tool broke - search again tomorrow
            day += 1
            print("You wait until the next day and search again.")
            pause(3)
            continue

        print("That will not fix the plane today.")
        print("You wait until the next day and search again.")
        day += 1
        pause(3)


def attempt_repair_with_game(problem_data, day):
    # Play a mini-game to repair the plane with the found tool. One try only!
    # Returns day if successful, None if game was lost.
    clear_console()
    print(f"You found the {problem_data['required_item']}!\n")
    print("Now you must use it correctly. You only get ONE chance.\n")
    print("(Press Enter to start)\n")
    input()
    
    games = [play_tic_tac_toe, play_unscramble, play_math_puzzle, play_memory_game, play_reaction_test]
    game = random.choice(games)
    
    clear_console()
    if game():
        # Game won - repair succeeds
        print(problem_data["repair_text"])
        pause_and_clear(3)
        return day
    else:
        # Game lost - tool breaks
        print("Your tool breaks! You'll have to search for another part tomorrow.\n")
        pause(2)
        return None


def play_tic_tac_toe():
    # Simple tic-tac-toe. Player is X, AI is O. Returns True if player wins.
    board = [" " for _ in range(9)]
    
    def print_board():
        print("\n   1   2   3")
        print(f" 1  {board[0]} | {board[1]} | {board[2]}")
        print("   -----------")
        print(f" 2  {board[3]} | {board[4]} | {board[5]}")
        print("   -----------")
        print(f" 3  {board[6]} | {board[7]} | {board[8]}\n")
    
    def check_winner(player):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        return any(board[i] == board[j] == board[k] == player for i, j, k in wins)
    
    def get_ai_move():
        # AI tries to win, then blocks player, then takes center, then corners
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                if check_winner("O"):
                    return
                board[i] = " "
        
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                if check_winner("X"):
                    board[i] = "O"
                    return
                board[i] = " "
        
        if board[4] == " ":
            board[4] = "O"
            return
        
        corners = [0, 2, 6, 8]
        available_corners = [i for i in corners if board[i] == " "]
        if available_corners:
            board[random.choice(available_corners)] = "O"
            return
        
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                return
    
    print("Welcome to Tic Tac Toe! You are X, AI is O. Choose your position (1-9).\n")
    
    while True:
        print_board()
        
        # Player move
        while True:
            try:
                pos = int(input("Your move (1-9): ")) - 1
                if 0 <= pos <= 8 and board[pos] == " ":
                    board[pos] = "X"
                    break
                print("Invalid move!")
            except ValueError:
                print("Enter a number 1-9.")
        
        if check_winner("X"):
            print_board()
            print("You won! Your tool is repaired perfectly!\n")
            return True
        
        if " " not in board:
            print_board()
            print("It's a draw! Your tool breaks from the stress of the repair.\n")
            return False
        
        # AI move
        get_ai_move()
        
        if check_winner("O"):
            print_board()
            print("AI won! Your tool breaks during the repair attempt.\n")
            return False
        
        if " " not in board:
            print_board()
            print("It's a draw! Your tool breaks from the stress of the repair.\n")
            return False


def play_unscramble():
    # Unscramble letters game. Returns True if player guesses correctly.
    words = ["ENGINE", "PROPELLER", "WING", "FUEL", "HYDRAULIC", "AIRCRAFT", "TURBINE", "LANDING", "REPAIR"]
    word = random.choice(words)
    scrambled = list(word)
    random.shuffle(scrambled)
    
    print(f"Unscramble the letters to fix your plane correctly!")
    print(f"Scrambled: {''.join(scrambled)}")
    print(f"Hint: The word has {len(word)} letters.\n")
    
    guess = input("Your guess (or 'hint' for hint): ").upper().strip()
    
    if guess == "hint":
        print(f"Hint: This is related to aircraft maintenance.")
        guess = input("Your guess: ").upper().strip()
    
    if guess == word:
        print(f"Correct! The word is '{word}'. Your repair is successful!\n")
        return True
    else:
        print(f"Wrong! The word was '{word}'. Your tool breaks from frustration.\n")
        return False


def play_math_puzzle():
    # Solve a quick math problem. Returns True if correct.
    num1 = random.randint(10, 50)
    num2 = random.randint(5, 20)
    operations = [
        (f"{num1} + {num2}", num1 + num2),
        (f"{num1} - {num2}", num1 - num2),
        (f"{num1} * {num2}", num1 * num2),
        (f"{num1} / {num2}", num1 // num2),
    ]
    
    problem, answer = random.choice(operations)
    
    print("Quick! Solve this math problem to calibrate your tools:")
    print(f"{problem} = ?\n")
    
    try:
        guess = int(input("Your answer: "))
        if guess == answer:
            print(f"Correct! {problem} = {answer}. Your repair is successful!\n")
            return True
        else:
            print(f"Wrong! {problem} = {answer}. Your tool breaks from the mistake.\n")
            return False
    except ValueError:
        print("Invalid input! Your tool breaks while you fumble around.\n")
        return False


def play_memory_game():
    # Memory sequence game. Returns True if player repeats the sequence
    sequence = []
    
    print("Memory Game! Watch the sequence of numbers:")
    print("(Press Enter to start)\n")
    input()
    
    for round_num in range(1, 4):
        sequence.append(random.randint(1, 9))
        print(f"Round {round_num}: {' -> '.join(map(str, sequence))}")
        pause(2)
        clear_console()
        
        guess = input(f"Repeat the sequence (separated by spaces): ").strip().split()
        
        try:
            guess = [int(x) for x in guess]
            if guess == sequence:
                print("Correct!\n")
                pause(1)
                clear_console()
            else:
                print(f"Wrong! The sequence was {' -> '.join(map(str, sequence))}. Your tool breaks.\n")
                return False
        except ValueError:
            print("Invalid input! Your tool breaks.\n")
            return False
    
    print("Perfect! You remembered the entire sequence. Your repair is successful!\n")
    return True


def play_reaction_test():
    # Type the word before time runs out. Returns True if fast enough.
    words = ["AIRCRAFT", "TURBINE", "REPAIR", "PROPELLER", "LANDING", "FUEL", "ENGINE"]
    word = random.choice(words)
    
    print("Reaction Test! Type this word as fast as you can:")
    print(f"\n{word}\n")
    print("Type it now (GO!):")
    
    import time
    start = time.time()
    guess = input().upper().strip()
    elapsed = time.time() - start
    
    if guess == word and elapsed < 5:
        print(f"Excellent! You typed it in {elapsed:.2f} seconds. Your repair is successful!\n")
        return True
    elif guess == word:
        print(f"Too slow! You took {elapsed:.2f} seconds. Your tool breaks.\n")
        return False
    else:
        print(f"Wrong word! Your tool breaks.\n")
        return False


def repair_plane(damage_key, inventory, day):
    problem_data = REPAIR_PROBLEMS[damage_key]
    required_item = problem_data["required_item"]

    clear_console()
    print("Your plane is damaged and you have to land.\n")
    print(f"{problem_data['problem']}\n")
    pause(7)

    if required_item in inventory:
        # Let the player use a spare part they found on an earlier day.
        print(f"You already have a {required_item} in your inventory.")
        inventory.remove(required_item)
        print("Now you must use it correctly to repair the plane.\n")
        pause(1)
        return attempt_repair_with_game(problem_data, day)

    # Must search for the required item first
    return search_for_repair_item(problem_data, inventory, day)


def complete_leg(progress, day):
    progress += LEG_PROGRESS
    day += TRAVEL_DAYS_PER_LEG

    print("You complete another leg of the trip.\n")
    print(f"You have now travelled {progress}% of the way around the world.")
    print(f"You have {WORLD_PROGRESS - progress}% left to go.\n")
    print("You Park the plane and rest for the day.\n")
    time.sleep(7)
    clear_console()
    print(f"It is now day {day}.\n")
    pause_and_clear(7)
    return progress, day


def play_game():
    progress = 0
    day = 1
    inventory = []

    # Keep flying new legs until the trip around the world is complete.
    while progress < WORLD_PROGRESS:
        clear_console()
        show_status(day, progress, inventory)
        show_takeoff_scene(day, progress)

        damage_key = choose_flight_problem()
        if damage_key is not None:
            day = repair_plane(damage_key, inventory, day)
            continue

        progress, day = complete_leg(progress, day)

    clear_console()
    print(f"You made it around the world in {day - 1} days!")  # type: ignore
    print("Your plane is battered, but you win the race.\n")


def main():
    clear_console()
    if show_intro():
        play_game()

# Game loop


if __name__ == "__main__":
    main()
