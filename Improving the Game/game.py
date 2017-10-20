#!/usr/bin/python3

from map import rooms
from player import *
from items import *
from gameparser import *


def print_separator():
    print()


def list_of_items(items):
    """This function takes a list of items (see items.py for the definition) and
    returns a comma-separated list of item names (as a string). For example:

    >>> list_of_items([item_pen, item_handbook])
    'a pen, a student handbook'

    >>> list_of_items([item_id])
    'id card'

    >>> list_of_items([])
    ''

    >>> list_of_items([item_money, item_handbook, item_laptop])
    'money, a student handbook, laptop'

    """

    separator = ", "
    items_names = []

    for item in items:
        items_names.append(item["name"])

    return separator.join(items_names)


def print_room_items(room):
    """This function takes a room as an input and nicely displays a list of items
    found in this room (followed by a blank line). If there are no items in
    the room, nothing is printed. See map.py for the definition of a room, and
    items.py for the definition of an item. This function uses list_of_items()
    to produce a comma-separated list of item names. For example:

    >>> print_room_items(rooms["Reception"])
    There is a pack of biscuits, a student handbook here.
    <BLANKLINE>

    >>> print_room_items(rooms["Office"])
    There is a pen here.
    <BLANKLINE>

    >>> print_room_items(rooms["Admins"])

    (no output)

    Note: <BLANKLINE> here means that doctest should expect a blank line.

    """

    if not room["items"]:
        return

    print("There is {0} here.".format(list_of_items(room["items"])))
    print_separator()


def print_inventory_items(items):
    """This function takes a list of inventory items and displays it nicely, in a
    manner similar to print_room_items(). The only difference is in formatting:
    print "You have ..." instead of "There is ... here.". For example:

    >>> print_inventory_items(inventory)
    You have id card, laptop, money.
    <BLANKLINE>

    """

    if not items:
        return

    print("You have {0}.".format(list_of_items(items)))
    print_separator()


def print_room(room):
    """This function takes a room as an input and nicely displays its name
    and description. The room argument is a dictionary with entries "name",
    "description" etc. (see map.py for the definition). The name of the room
    is printed in all capitals and framed by blank lines. Then follows the
    description of the room and a blank line again. If there are any items
    in the room, the list of items is printed next followed by a blank line
    (use print_room_items() for this). For example:

    >>> print_room(rooms["Office"])
    <BLANKLINE>
    THE GENERAL OFFICE
    <BLANKLINE>
    You are standing next to the cashier's till at
    30-36 Newport Road. The cashier looks at you with hope
    in their eyes. If you go west you can return to the
    Queen's Buildings.
    <BLANKLINE>
    There is a pen here.
    <BLANKLINE>

    >>> print_room(rooms["Reception"])
    <BLANKLINE>
    RECEPTION
    <BLANKLINE>
    You are in a maze of twisty little passages, all alike.
    Next to you is the School of Computer Science and
    Informatics reception. The receptionist, Matt Strangis,
    seems to be playing an old school text-based adventure
    game on his computer. There are corridors leading to the
    south and east. The exit is to the west.
    <BLANKLINE>
    There is a pack of biscuits, a student handbook here.
    <BLANKLINE>

    >>> print_room(rooms["Admins"])
    <BLANKLINE>
    MJ AND SIMON'S ROOM
    <BLANKLINE>
    You are leaning agains the door of the systems managers'
    room. Inside you notice Matt "MJ" John and Simon Jones. They
    ignore you. To the north is the reception.
    <BLANKLINE>

    Note: <BLANKLINE> here means that doctest should expect a blank line.
    """
    # Display room name
    print_separator()
    print(room["name"].upper())
    print_separator()
    # Display room description
    print(room["description"])
    print_separator()

    if room["items"]:
        print_room_items(room)


def exit_leads_to(exits, direction):
    """This function takes a dictionary of exits and a direction (a particular
    exit taken from this dictionary). It returns the name of the room into which
    this exit leads. For example:

    >>> exit_leads_to(rooms["Reception"]["exits"], "south")
    "MJ and Simon's room"
    >>> exit_leads_to(rooms["Reception"]["exits"], "east")
    "your personal tutor's office"
    >>> exit_leads_to(rooms["Tutor"]["exits"], "west")
    'Reception'
    """
    return rooms[exits[direction]]["name"]


def print_exit(direction, leads_to):
    """This function prints a line of a menu of exits. It takes a direction (the
    name of an exit) and the name of the room into which it leads (leads_to),
    and should print a menu line in the following format:

    GO <EXIT NAME UPPERCASE> to <where it leads>.

    For example:
    >>> print_exit("east", "you personal tutor's office")
    GO EAST to you personal tutor's office.
    >>> print_exit("south", "MJ and Simon's room")
    GO SOUTH to MJ and Simon's room.
    """
    print("GO " + direction.upper() + " to " + leads_to + ".")


def print_menu(exits, room_items, inv_items):
    """This function displays the menu of available actions to the player. The
    argument exits is a dictionary of exits as exemplified in map.py. The
    arguments room_items and inv_items are the items lying around in the room
    and carried by the player respectively. The menu should, for each exit,
    call the function print_exit() to print the information about each exit in
    the appropriate format. The room into which an exit leads is obtained
    using the function exit_leads_to(). Then, it should print a list of commands
    related to items: for each item in the room print

    "TAKE <ITEM ID> to take <item name>."

    and for each item in the inventory print

    "DROP <ITEM ID> to drop <item name>."

    For example, the menu of actions available at the Reception may look like this:

    You can:
    GO EAST to your personal tutor's office.
    GO WEST to the parking lot.
    GO SOUTH to MJ and Simon's room.
    TAKE BISCUITS to take a pack of biscuits.
    TAKE HANDBOOK to take a student handbook.
    DROP ID to drop your id card.
    DROP LAPTOP to drop your laptop.
    DROP MONEY to drop your money.
    What do you want to do?

    """
    print("You can:")
    # Iterate over available exits
    for direction in exits:
        # Print the exit name and where it leads to
        print_exit(direction, exit_leads_to(exits, direction))

    for room_item in room_items:
        print("TAKE {0} to take {1}".format(room_item["id"].upper(), room_item["name"]))

    for inv_item in inv_items:
        print("DROP {0} to drop {1}".format(inv_item["id"].upper(), inv_item["name"]))

    print("What do you want to do?")


def is_valid_exit(exits, chosen_exit):
    """This function checks, given a dictionary "exits" (see map.py) and
    a players's choice "chosen_exit" whether the player has chosen a valid exit.
    It returns True if the exit is valid, and False otherwise. Assume that
    the name of the exit has been normalised by the function normalise_input().
    For example:

    >>> is_valid_exit(rooms["Reception"]["exits"], "south")
    True
    >>> is_valid_exit(rooms["Reception"]["exits"], "up")
    False
    >>> is_valid_exit(rooms["Parking"]["exits"], "west")
    False
    >>> is_valid_exit(rooms["Parking"]["exits"], "east")
    True
    """
    return chosen_exit in exits


def execute_go(direction):
    """This function, given the direction (e.g. "south") updates the current room
    to reflect the movement of the player if the direction is a valid exit
    (and prints the name of the room into which the player is
    moving). Otherwise, it prints "You cannot go there."
    """

    global current_room

    if not is_valid_exit(current_room["exits"], direction):
        print("You cannot go there.")
        return

    new_room = move(current_room["exits"], direction)

    print("Moving into {0}.".format(new_room["name"]))

    current_room = new_room


def execute_take(item_id):
    """This function takes an item_id as an argument and moves this item from the
    list of items in the current room to the player's inventory. However, if
    there is no such item in the room, this function prints
    "You cannot take that."
    """

    item_exists = False
    item = None

    for item_in_room in current_room["items"]:
        if item_in_room["id"] == item_id:
            item_exists = True
            item = item_in_room
            break

    if not item_exists:
        print("You cannot take that.")
        return

    if item["mass"] + get_items_weight(inventory) > MAX_WEIGHT_TO_CARRY:
        print("You can't carry more weight. Drop another item first.")
        return

    current_room["items"].remove(item)
    inventory.append(item)


def execute_drop(item_id):
    """This function takes an item_id as an argument and moves this item from the
    player's inventory to list of items in the current room. However, if there is
    no such item in the inventory, this function prints "You cannot drop that."
    """

    player_has_item = False
    item = None

    for item_in_inventory in inventory:
        if item_in_inventory["id"] == item_id:
            player_has_item = True
            item = item_in_inventory
            break

    if not player_has_item:
        print("You cannot drop that.")
        return

    inventory.remove(item)
    current_room["items"].append(item)


def execute_command(command):
    """This function takes a command (a list of words as returned by
    normalise_input) and, depending on the type of action (the first word of
    the command: "go", "take", or "drop"), executes either execute_go,
    execute_take, or execute_drop, supplying the second word as the argument.

    """

    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")

    else:
        print("This makes no sense.")


def menu(exits, room_items, inv_items):
    """This function, given a dictionary of possible exits from a room, and a list
    of items found in the room and carried by the player, prints the menu of
    actions using print_menu() function. It then prompts the player to type an
    action. The players's input is normalised using the normalise_input()
    function before being returned.

    """

    # Display menu
    print_menu(exits, room_items, inv_items)

    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits, direction):
    """This function returns the room into which the player will move if, from a
    dictionary "exits" of avaiable exits, they choose to move towards the exit
    with the name given by "direction". For example:

    >>> move(rooms["Reception"]["exits"], "south") == rooms["Admins"]
    True
    >>> move(rooms["Reception"]["exits"], "east") == rooms["Tutor"]
    True
    >>> move(rooms["Reception"]["exits"], "west") == rooms["Office"]
    False
    """

    # Next room to go to
    return rooms[exits[direction]]


def get_items_weight(items):
    total = 0

    for item in items:
        total += item["mass"]

    return total


# This is the entry point of our program
def main():
    global current_room
    laptop_is_in_admins_room = False
    tutor_has_biscuits = False
    showed_id_to_reception = False

    print_welcome_screen()

    # Main game loop
    while True:

        if current_room == rooms["Office"] and item_id not in inventory:
            print("You need your id to access the office!")
            current_room = rooms["Parking"]
            continue

        print_room(current_room)

        if current_room == rooms["Admins"] and laptop_is_in_admins_room:
            print("Your laptop is here and the Admins are playing around with it. They are very happy.")

        if current_room == rooms["Tutor"] and tutor_has_biscuits:
            print("Your tutor is happy because she has biscuits. Good job!")

        if current_room == rooms["Reception"] and showed_id_to_reception:
            print("You showed your id to reception. They're happy that there are no strangers roaming the buildings.")
            if item_id in rooms["Reception"]["items"]:
                print("You may take your id now.")

        print_inventory_items(inventory)
        print("You carry {0} kg".format(get_items_weight(inventory)))

        # Show the menu with possible actions and ask the player
        command = menu(current_room["exits"], current_room["items"], inventory)

        # Execute the player's command
        execute_command(command)

        if item_id in rooms["Reception"]["items"]:
            showed_id_to_reception = True

        laptop_is_in_admins_room = item_laptop in rooms["Admins"]["items"]
        tutor_has_biscuits = item_biscuits in rooms["Tutor"]["items"]

        if laptop_is_in_admins_room and \
                tutor_has_biscuits and \
                showed_id_to_reception and \
                item_pen in inventory and \
                item_handbook in inventory:

            print_ending_screen()
            break


def print_welcome_screen():
    welcome_message = """WELCOME TO THE ADVENTURE!
Your goal is to make everyone you meet happy. But don't forget to collect all items a student needs!
Have fun!
    """

    print_separator()
    print(welcome_message)
    print_separator()


def print_ending_screen():
    you_win_message =  """
\   //~~\ |   |  |  |  |~|~|\  |  |\  | /~~\~~|~~|  |~|~|\  | /~~\\
 \ /|    ||   |  |  |  | | | \ |  | \ ||    | |  |--| | | \ ||  __
  |  \__/  \_/    \/ \/ _|_|  \|  |  \| \__/  |  |  |_|_|  \| \__/    
    """
    secret_message = "Jngpu Ze. Ebobg. cym"
    print(you_win_message)
    print(secret_message)


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()
