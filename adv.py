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

player = Player(world.starting_room)

# search the graph
def breadth_first_search():
    # empty queue with a Path
    queue = [[player.current_room]]
    
    # visited rooms
    visited_rooms = {}

    # track ? rooms
    questionable_rooms = set()
    questionable_rooms.add(player.current_room.id)

    # for loop to get the room exits for starting room
    # outisde of while loop for effiecency sake
    # this sets up inner dictonary
    visited_rooms[player.current_room.id] = {}

    for door in player.current_room.get_exits():
        visited_rooms[player.current_room.id][door] = '?'

    continue_loop = True

    # while the ? tracker is NOT empty
    while continue_loop:
        # dequeue the current PATH from the front of the queue
        current_path = queue.pop(0) # creates a single list

        # get the current room to analyze from the end of the PATH
        # use the room at the END of the PATH array
        # this is a way to look at the last place we have been
        current_room = current_path[-1]
        # set the player to the last room in the PATH
        player.current_room = current_room

        # get the room numbers for each exit - go through rooms
        # getting only keys from inner dictonary
        for cardinal_direction in list(visited_rooms[current_room.id].keys()):
            # try a room
            player.travel(cardinal_direction)
            # get room id
            next_room = player.current_room
            # update inner dictonary for each cardinal directrion of the orginal room
            visited_rooms[current_room.id][cardinal_direction] = next_room.id
            
            # if the new room is not in the outer dictonary
            if next_room.id not in visited_rooms:
                # add new room to outer dictonary each time
                visited_rooms[next_room.id] = {}
                # set up '?'
                for door in next_room.get_exits():
                    visited_rooms[next_room.id][door] = '?'
                # add ? room to tracker
                questionable_rooms.add(next_room.id)
            else: # if the new room IS in the outer dictonary
                # check if there are any ? doors
                if next_room.id in questionable_rooms:
                    if '?' not in set(visited_rooms[next_room.id].values()):
                        # remove from ? tracker
                        questionable_rooms.remove(next_room.id)
                

            # update inner dictonary with pervious room id
            # hard code where the player came from
            if cardinal_direction == 'n':
                visited_rooms[next_room.id]['s'] = current_room.id
            elif cardinal_direction == 's':
                visited_rooms[next_room.id]['n'] = current_room.id
            
            elif cardinal_direction == 'e':
                visited_rooms[next_room.id]['w'] = current_room.id
            elif cardinal_direction == 'w':
                visited_rooms[next_room.id]['e'] = current_room.id     

            
            # save a copy of current PATH with new room id
            # COPY  the current PATH
            current_path_copy = list(current_path)
            # add the available room to the new path
            current_path_copy.append(next_room)
            # add the whole PATH to the queue
            queue.append(current_path_copy)

            if len(set(room.id for room in current_path_copy)) >= len(room_graph):
                continue_loop = False
                current_path = current_path_copy
                break
        
            # go back to pervious room
            player.current_room = current_room

    # invert only inner dictonary key <-- values
    for key in visited_rooms.keys(): # keys of outer dictonary = room ids
        visited_rooms[key] = {v: k for k, v in visited_rooms[key].items()} 

    # preperations
    # remove the first room 
    last_room = current_path.pop(0)
    # list for cardinal directions
    bird = []

    # convert room id --> cardinal directions
    for room in current_path:
        bird.append(visited_rooms[last_room.id][room.id])
        last_room = room

    return bird

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = breadth_first_search()

# Print an ASCII map
world.print_rooms()
print(traversal_path)

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
player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
