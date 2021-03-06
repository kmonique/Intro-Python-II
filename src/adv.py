from room import Room
from player import Player
from item import Item

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons",
                [Item("sword", "this sword has dull edges")]),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""",[Item("bow", "a bow with no arrows")]),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""",[Item("arrows", "a box of arrows are neatly stored here")]),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""",[Item("gun", "the gun is jammed")]),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""", [Item("longsword", "this sword has sharp edges")]),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

import textwrap

# grabs user input
def grab_input():
    command = input("\nPlease enter an action: ")
    command = command.strip().lower().split(" ")
    if len(command) < 2:
        if command[0] == "q":
            exit()
        elif command[0] in ["n", "s", "e", "w"]:
            return command[0]
        elif command[0] in ["i", "inventory"]:
            print(f"Current Inventory: {player.inventory}")
        else:
            print("Invalid entry! Please use 'n', 's', 'e' or 'w' to navigate rooms\nEnter 'i' to view the rooms inventory\nEnter 'q' to exit the game")
            grab_input()
    else:
        if command[0] in ["get", "take"]:
            add_item(command[1])
        elif command[0] == "drop":
            drop_item(command[1])
        else:
            print("Invalid action: ")
            grab_input()

# add item to player inventory and remove it from room
def add_item(item):
    for i, val in enumerate(player.current_room.items):
        if str(item) == str(val):
            player.inventory.append(player.current_room.items[i])
            player.current_room.items[i].on_take(val)
            player.current_room.items.remove(val)
        elif i >= len(player.current_room.items) - 1:
            print("\nItem not in room\n")

# drop item from player inventory and add it to room
def drop_item(item):
    for i, val in enumerate(player.inventory):
        if str(item) == str(val):
            player.current_room.items.append(val)
            player.inventory.remove(val)
            player.current_room.items[i].on_drop(item)
        elif i >= len(player.current_room.items) - 1:
            print("\nItem not in inventory\n")

# checks to see if room has direction attribute
def try_direction(direction, current_room):
    attribute = direction + "_to"

    if hasattr(current_room, attribute):
        return getattr(current_room, attribute)
    else:
        print(direction_error(direction))
        return current_room

# error messages for invalid room directions
def direction_error(direction):
    if direction == "n":
        return "There is no room to the North\n"
    elif direction == "s":
        return "There is no room to the South\n"
    elif direction == "e":
        return "There is no room to the East\n"
    elif direction == "w":
        return "There is no room to the West\n"
    else:
        return "Goodbye!"

# message for room items
def print_items(item_list):
    if len(item_list) > 0:
        for i, val in enumerate(item_list):
            print(f"A {item_list[i]} can be found in this room. " +
            f"To take the {item_list[i]}, type 'get [item name]' or 'take [item name]' ")
        
print("Welcome to the game!\n")
username = input("Please enter your players name: ")
print(f"\nHello {username}, within this game you can navigate rooms using n, s, w, or e\n")

# Make a new player object that is currently in the 'outside' room.
player = Player(username, room["outside"])

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
action = None

while (action != "q"):
    print("Current Position: " + 
        textwrap.fill(player.current_room.name + 
        ". " + player.current_room.description, width=50))
    print_items(player.current_room.items)
    action = grab_input()
    if action in ["n", "s", "e", "w"]:
        player.current_room = try_direction(action, player.current_room)