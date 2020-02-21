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
        self.visited_rooms = []
        self.new_rooms = []
        self.path = []
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y
        self.weight = 0
        self.dead_end = False
        self.dead_end_in = []
        self.dead_end_out = []
        self.is_dead_end_node = False
        self.is_dead_end_root_node = False

    def set_dead_end_root_node(self):
        self.is_dead_end_root_node = True

    def set_dead_end_in_node(self, in_node, out_dir):
        # print(
        #     f"Set dead end next: {self.id}  {direction} -> {next_dead_end_node.id}")
        self.try_to_remove_unvisited_dir(opposites[out_dir])
        self.is_dead_end_node = True
        node = {"room": in_node.id, "direction": opposites[out_dir]}
        self.dead_end_in = self.check_for_current_node(self.dead_end_in, node)
        in_node.set_dead_end_out_node(self, out_dir)

    def set_dead_end_out_node(self, out_node, out_dir):
        # print(
        #     f"Set dead end next: {self.id}  {direction} -> {next_dead_end_node.id}")
        self.try_to_remove_unvisited_dir(out_dir)
        node = {"room": out_node.id, "direction": out_dir}
        self.dead_end_out = self.check_for_current_node(self.dead_end_out,
                                                        node)

    def check_for_current_node(self, nodes, node):
        found = False
        for each in nodes:
            if each['room'] == node['room']:
                print("Found the node")
                found = True

        if not found:
            nodes.append(node)

        return nodes

    def try_to_remove_unvisited_dir(self, dir):
        if dir in self.unvisited_directions:
            self.unvisited_directions.remove(dir)
        else:
            print("Trying to remove a dir that has already been removed.")

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
