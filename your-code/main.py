import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from datetime import datetime
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from time import sleep

import update_db as mydb

# get path of sound files
relative_path = os.getcwd()
game_sound = relative_path + '/your-code/sound/time.wav'
end_sound = relative_path + '/your-code/sound/do_it_end.wav'

# open image with game map
ImageAddress = relative_path + "/new_map.jpg"
ImageItself = Image.open(ImageAddress)
ImageNumpyFormat = np.asarray(ImageItself)
plt.figure(figsize=(12, 5), dpi=100)
plt.imshow(ImageNumpyFormat)
plt.axis('off')
plt.draw()
plt.pause(1)

# set music player depending on OS
player = "afplay " if os.name == 'posix' else "start "


pygame.mixer.init()
pygame.mixer.music.load(game_sound)
pygame.mixer.music.play()

# define rooms and items
whiteboard = {
    "name": "whiteboard",
    "type": "furniture"
}

python_project = {
    "name": "python project",
    "type": "door"
}

tableau_project = {
    "name": "tableau project",
    "type": "door"
}

ai_project = {
    "name": "AI project",
    "type": "door"
}

graduation_d = {
    "name": "graduation",
    "type": "door",
}

python = {
    "name": "python for python project",
    "type": "key",
    "target": python_project
}

tableau = {"name": "tableau for tableau project",
           "type": "key",
           "target": tableau_project
           }

sklearn = {"name": "sklearn for AI project",
           "type": "key",
           "target": ai_project
           }

soft_skills = {"name": "soft skills",
               "type": "key",
               "target": graduation_d
               }

computer = {
    "name": "computer",
    "type": "furniture",
}

mod_1 = {
    "name": "module 1",
    "type": "room"
}

grad_party = {
    "name": "grad_party"
}

mod_2 = {"name": "module 2",
         "type": "room"
         }

mod_3 = {"name": "module 3",
         "type": "room"
         }

career_hack = {"name": "careerhack",
               " type": "room"
               }

lecture_1 = {"name": "lecture",
             "type": "furniture"
             }

presentation_1 = {"name": "presentation",
                  "type": "furniture"
                  }

# lab = {"name": "lab",
#       "type": "furniture"
#       }

one_on_one = {"name": "one-on-one",
              "type": "furniture"
              }

all_rooms = [mod_1, grad_party, mod_2, mod_3, career_hack]

all_doors = [python_project, tableau_project, ai_project, graduation_d]

# define which items/rooms are related

object_relations = {
    "module 1": [whiteboard, computer, python_project],
    "computer": [python],
    "grad_party": [graduation_d],
    "python project": [mod_1, mod_2],
    "module 2": [lecture_1, python_project, tableau_project],
    "lecture": [tableau],
    "tableau project": [mod_2, mod_3],
    "module 3": [presentation_1, tableau_project, ai_project],
    "presentation": [sklearn],
    "one-on-one": [soft_skills],
    "AI project": [career_hack, mod_3],
    "careerhack": [one_on_one, graduation_d, ai_project],
    "graduation": [grad_party]
}

# define game state. Do not directly change this dict.
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": mod_1,
    "keys_collected": [],
    "target_room": grad_party
}

try:
    def screen_clear():
        # for mac and linux
        if os.name == 'posix':
            _ = os.system('clear')
        else:
            # for windows
            _ = os.system('cls')

    def linebreak():
        """
        Print a line break
        """
        print("\n\n")

    def start_game():
        """
        Start the game
        """
        global startTime, user
        screen_clear()
        startTime = datetime.now()
        print("\n\n\nWelcome!\nYou have entered the Ironhack Data Analytics Bootcamp!\nIts 9 weeks long and you must give it all!\nYou have never done this before, but you feel excited to learn\nTry to graduate NOW!\n")
        user = input("\nPlease enter your name: ").strip()
        play_room(game_state["current_room"])

    def play_room(room):
        """
        Play a room. First check if the room being played is the target room.
        If it is, the game will end with success. Otherwise, let player either 
        explore (list all items in this room) or examine an item found here.
        """
        game_state["current_room"] = room
        if(game_state["current_room"] == game_state["target_room"]):
            seconds = (datetime.now() - startTime).total_seconds()
            total_time = round(seconds,1)
            mydb.update_database([user,total_time])
            print(
                f"\nCongrats! You escaped the room in {total_time} seconds!")
            os.system(player + end_sound)
            
            # Call method from our library to show the leaderboard
            mydb.show_leaders()
            sleep(10)
            plt.close()
        else:
            print("You are now in " + room["name"])
            intended_action = input(
                "\nWhat would you like to do? Explore [1] or Examine [2] ? ").strip()
            if intended_action.lower() == "1":
                explore_room(room)
                play_room(room)
            elif intended_action.lower() == "2":
                examine_item(
                    input("\nWhat would you like to examine?").strip())
            else:
                print("\nNot sure what you mean. Explore [1] or Examine [2] ?")
                play_room(room)
            linebreak()

    def explore_room(room):
        """
        Explore a room. List all items belonging to this room.
        """
        items = [i["name"] for i in object_relations[room["name"]]]
        print("\nYou explore it. This is " +
              room["name"] + ". You find " + ", ".join(items))

    def get_next_room_of_door(door, current_room):
        """
        From object_relations, find the two rooms connected to the given door.
        Return the room that is not the current_room.
        """
        connected_rooms = object_relations[door["name"]]
        for room in connected_rooms:
            if(not current_room == room):
                return room

    def examine_item(item_name):
        """
        Examine an item which can be a door or furniture.
        First make sure the intended item belongs to the current room.
        Then check if the item is a door. Tell player if key hasn't been 
        collected yet. Otherwise ask player if they want to go to the next
        room. If the item is not a door, then check if it contains keys.
        Collect the key if found and update the game state. At the end,
        play either the current or the next room depending on the game state
        to keep playing.
        """
        current_room = game_state["current_room"]
        next_room = ""
        output = None

        for item in object_relations[current_room["name"]]:
            if(item["name"].lower() == item_name.strip().lower()):
                output = "\nYou examine " + item_name.strip().lower() + ". "
                if(item["type"] == "door"):
                    have_key = False
                    for key in game_state["keys_collected"]:
                        if(key["target"] == item):
                            have_key = True
                    if(have_key):
                        output += "\nYou delivered the project!"
                        next_room = get_next_room_of_door(item, current_room)
                    else:
                        output += "\nIt is locked but you don't have the key."
                else:
                    if(item["name"] in object_relations and len(object_relations[item["name"]]) > 0):
                        item_found = object_relations[item["name"]].pop()
                        game_state["keys_collected"].append(item_found)
                        output += "\nYou find " + item_found["name"] + "."
                    else:
                        output += "\nThere isn't anything interesting about it."
                print(output)
                break

        if(output is None):
            print("\nThe item you requested is not found in the current room.")

        if(next_room and input("\nDo you want to go to the next module? Yes [y] or No [n]: ").strip().lower() == 'y'):
            play_room(next_room)
        else:
            play_room(current_room)

    game_state = INIT_GAME_STATE.copy()
    print("\n"*100)
    start_game()
except KeyboardInterrupt:
    plt.close()
    print("You interrupted the program execution.")
