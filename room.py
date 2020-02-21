import random

# Implement a class to hold room information. This should have name and
# description attributes.
opposites = {"n": "s", "s": "n", "e": "w", "w": "e"}


class Room:
    def __init__(self, name, description, id = 0, x = None, y = None):
        self.id = id
        self.name = name
        self.description = description
        self.unvisited_directions = []
        self.new_rooms = []
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y
        self.weight = 0
        self.path = []
        self.dead_end_next_direction = None
        self.dead_end_prev_direction = None
        self.dead_end_prev = None
        self.dead_end_node = None
        self.dead_end_next = None
        self.is_dead_end_node = False
        self.visited_rooms = {}

    def set_dead_end_next(self, next_dead_end_node, direction):
        # print(
        #     f"Set dead end next: {self.id}  {opposites[direction]} -> {next_dead_end_node.id}")
        self.dead_end_next = next_dead_end_node
        self.dead_end_next_direction = opposites[direction]

    def set_up_dead_end_prev(self, dead_end, direction):
        # print(
        #     f"Set dead end prev: {self.id} {direction} -> {dead_end.id}")
        self.dead_end_prev = dead_end
        self.dead_end_prev_direction = direction

    def __str__(self):
        return f"\n-------------------\n\n{self.name}\n\n   {self.description}\n\n{self.get_exits_string()}\n"

    def print_room_description(self, player):
        print(str(self))

    def get_exits(self, unvisited_eixts_only = True):

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
        if direction not in self.unvisited_directions:
            self.add_unvisited_direction(direction)
        if opposites[direction] not in connecting_room.unvisited_directions:
            connecting_room.add_unvisited_direction(opposites[direction])

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

    def get_and_remove_room_in_direction(self, direction, log_error):
        # print(f"Removing route {direction} from {self.id}")
        room = self.get_room_in_direction(direction)

        not_in = direction not in self.unvisited_directions
        if not_in:
            if not log_error:
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

    def get_coords(self):
        return [self.x, self.y]
