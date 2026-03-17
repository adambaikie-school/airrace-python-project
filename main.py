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


def pause(seconds=2):
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
    pause_and_clear(6)
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
    if random.random() < 0.5:
        return handle_takeoff_problem()
    return handle_air_event()


def get_search_options(required_item):
    # The correct repair item only appears some of the time, which can push repairs into the next day.
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
            # Remove the part once it is used so the player has to find it again next time.
            inventory.remove(required_item)
            print(problem_data["repair_text"])
            pause_and_clear(3)
            return day

        print("That will not fix the plane today.")
        print("You wait until the next day and search again.")
        day += 1
        pause(3)


def repair_plane(damage_key, inventory, day):
    problem_data = REPAIR_PROBLEMS[damage_key]
    required_item = problem_data["required_item"]

    clear_console()
    print("Your plane is damaged and you have to land.\n")
    print(f"{problem_data['problem']}\n")
    pause(3)

    if required_item in inventory:
        # Let the player use a spare part they found on an earlier day.
        print(f"You already have a {required_item} in your inventory.")
        inventory.remove(required_item)
        print(problem_data["repair_text"])
        pause_and_clear(3)
        return day

    return search_for_repair_item(problem_data, inventory, day)


def complete_leg(progress, day):
    progress += LEG_PROGRESS
    day += TRAVEL_DAYS_PER_LEG

    print("You complete another leg of the trip.\n")
    print(f"You have now travelled {progress}% of the way around the world.")
    print(f"It is now day {day}.\n")
    pause_and_clear(3)
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
    print(f"You made it around the world in {day - 1} days!")
    print("Your plane is battered, but you win the race.\n")


def main():
    clear_console()
    if show_intro():
        play_game()

# Game loop

if __name__ == "__main__":
    main()
