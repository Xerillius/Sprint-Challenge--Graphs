from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
room_keys = {}
unknown = {}
reverse = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
directions = ['n', 'e', 's', 'w']
trail = []

def set_doors():
    doors = {}
    for door in player.current_room.get_exits():
        doors[door] = '?'
    return doors

# Remove explored rooms from unknown dict
def update_unknown():
    rooms_to_del = []
    for key in unknown:
        del_room = True
        for direction in unknown[key]:
            if unknown[key][direction] == '?':
                del_room = False
        if del_room:
            rooms_to_del.append(key)
    for i in rooms_to_del:
        unknown.pop(i)

# Function to move in a direction
def move_direction(val, prev):
    # Move Player
    player.travel(val)
    # Set exits for room if not already there
    if player.current_room.id not in room_keys:
        # Get exits
        doors = set_doors()
        # Apply exits to room_keys and unknown
        room_keys[player.current_room.id] = doors
        unknown[player.current_room.id] = doors
    # Set key to previous room to previous room
    room_keys[player.current_room.id][reverse[val]] = prev
    # Set key in previous room leading to current room TO current room
    room_keys[prev][val] = player.current_room.id
    # Add movement to path
    traversal_path.append(val)

# This function is to be made recursive at a later date
# Will also use backtracking
def move_player(starting_room):
    if len(unknown) > 0:
        trail.append(starting_room)
        # Cycle through directions
        for direction in directions:
            if direction in room_keys[starting_room]:
                if room_keys[starting_room][direction] is '?':
                    move_direction(direction, starting_room)
                    # Set Traversal Index for this iteration
                    t_index = len(traversal_path) - 1
                    update_unknown()
                    move_player(player.current_room.id)
                    if len(unknown) > 0:
                        backtrack(t_index)
        return

def backtrack(t_index):
    move_direction(reverse[traversal_path[t_index]], player.current_room.id)
    trail.pop()

### ### ### INIT STARTING ROOM ### ### ###
room_keys[player.current_room.id] = set_doors()
unknown[player.current_room.id] = room_keys[player.current_room.id]
### ### ### ### ### ## ### ### ### ### ###

import time

start = time.time()
### RUN THE MAZE ###
move_player(player.current_room.id)
end = time.time()

print(end - start,"seconds")

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")