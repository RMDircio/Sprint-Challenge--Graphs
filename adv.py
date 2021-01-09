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

# search the graph
def breadth_first_traversal():
    # empty queue with a Path
    queue = [[player.current_room.id]]
    
    # visited rooms
    visited_rooms = {}

    # a way to track '?'
    questionable_rooms = set()

    # while the queue is NOT empty
    while len(queue) > 0:
        # dequeue the current PATH from the front of the queue
        current_path = queue.pop(0) # creates a single list

        # get the current room to analyze from the end of the PATH
        # use the room at the END of the PATH array
        current_room = current_path[-1]

        # if room has not been visited
        if current_room not in visited_rooms:
            # add to ? tracker
            questionable_rooms.add(current_room)
            
            # add room to visited list
            visited_rooms[current_room] = {}

            # for loop to get the room exits
            for door in player.current_room.get_exits():
                visited_rooms[current_room][door] = '?'

        # if the room HAS been visited
        else:
            pass
        
        # break
        if len(visited_rooms.keys()) == 500 and len(questionable_rooms) == 0:
            # invert only inner dictonary key <-- values
            for key in visited_rooms.keys(): # keys of outer dictonary = room ids
                visited_rooms[key] = {v: k for k, v in visited_rooms[key].items()} 

            # preperations
            # remove the first room 
            remove_zero_room = current_path.pop(0)
            # list for cardinal directions
            bird = []

            # convert room id --> cardinal directions
            for room in current_path:
                bird.append(visited_rooms[remove_zero_room][room])
                remove_zero_room = bird

            return bird


    # return current_path
    grapes = []
    print('Debugging Here')
    print(player.travel('n'))    
    print(player.current_room.id)
    print(player.current_room.get_exits())
    return grapes


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = breadth_first_traversal()
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
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
