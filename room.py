from typing import Dict, List
import random

opposites = {"s": "n", "n": "s", "e": "w", "w": "e"}


class Room(object):
    def __init__(self, name: str, description: str, id: enumerate = 0,
                 x: enumerate = None, y: enumerate = None) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.unvisited_directions = []
        self.visited_rooms = []
        self.path = []
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y
        self.visited = False
        self.weight = 0
        self.dead_end = False
        self.dead_end_in: Dict[str: Room] = {}
        self.dead_end_out: Dict[str: Room] = {}
        self.is_dead_end_node = False
        self.is_dead_end_root_node = False
        self.number_of_paths = 0
        self.number_of_dead_ends = 0

    def set_dead_end_in_node(self, in_node, out_dir: str):
        # print(
        #     f"Set dead end next: {self.id}  {direction} -> {next_dead_end_node.id}")
        self.try_to_remove_unvisited_dir(opposites[out_dir])
        self.is_dead_end_node = True
        self.dead_end_in[opposites[out_dir]] = in_node
        if len(self.dead_end_in) > self.number_of_dead_ends:
            self.number_of_dead_ends = len(self.dead_end_in)
        in_node.set_dead_end_out_node(self, out_dir)

    def set_dead_end_out_node(self, out_node, out_dir: str):
        # print(
        #     f"Set dead end next: {self.id}  {direction} -> {next_dead_end_node.id}")
        self.try_to_remove_unvisited_dir(out_dir)
        self.dead_end_out[out_dir] = out_node

    def try_to_remove_unvisited_dir(self, dir, print_error = False):
        if dir in self.unvisited_directions:
            self.unvisited_directions.remove(dir)
        else:
            if print_error:
                print("Trying to remove a dir that has already been removed.")

    def __str__(self):
        return f"\n-------------------\n\n{self.name}\n\n   {self.description}\n\n{self.get_exits_string()}\n"

    def print_room_description(self, player):
        print(str(self))

    def get_exits(self, unvisited_eixts_only: bool = False) -> List:

        exits = []
        if not unvisited_eixts_only:
            if self.n_to is not None:
                exits.append("n")
            if self.s_to is not None:
                exits.append("s")
            if self.w_to is not None:
                exits.append("w")
            if self.e_to is not None:
                exits.append("e")

            return exits

        else:
            if len(self.unvisited_directions) == 0:
                # print("Returning 0 avaiable directions")
                # print(f"{self.id}")
                exits = []
            else:
                for exit in self.unvisited_directions:
                    exits.append(exit)

            return exits

    def get_exits_string(self, ):
        return f"Exits: [{', '.join(self.get_exits(False))}]"

    def connect_rooms(self, direction, connecting_room):

        if direction == "n":
            self.n_to = connecting_room
            connecting_room.s_to = self
        elif direction == "s":
            self.s_to = connecting_room
            connecting_room.n_to = self
        elif direction == "e":
            self.e_to = connecting_room
            connecting_room.w_to = self
        elif direction == "w":
            self.w_to = connecting_room
            connecting_room.e_to = self
        else:
            print("INVALID ROOM CONNECTION")
            return None

    def add_unvisited_direction(self, direction):
        self.unvisited_directions.append(direction)

    def get_and_remove_room_in_direction(self, direction, hide_error):
        # print(f"Removing route {direction} from {self.id}")
        room = self.get_room_in_direction(direction)

        not_in = direction not in self.unvisited_directions
        if not_in:
            if not hide_error:
                print(
                    "That room has already been removed from the unvisited directoins")
                print(f"{self.id} Returning the room anyway. ")
        else:
            # print(f"Removing {direction} from {self.id}")
            self.unvisited_directions.remove(direction)
            self.visited_rooms[direction] = {"Other_id": room.id}

        return room

    def get_room_in_direction(self, direction):
        if direction == "n":
            return self.n_to
        elif direction == "s":
            return self.s_to
        elif direction == "e":
            return self.e_to
        elif direction == "w":
            return self.w_to
        else:
            return None

    def set_number_of_paths(self):
        paths = self.get_exits()
        self.number_of_paths = len(paths)

    def get_coords(self):
        return [self.x, self.y]
