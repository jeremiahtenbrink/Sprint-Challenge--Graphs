from util import Stack, Queue
from typing import List, Dict
import random
from room import Room

opposites = {"s": "n", "n": "s", "e": "w", "w": "e"}


class Player(object):
    def __init__(self, starting_room: Room, rooms: enumerate) -> None:
        self.starting_room: Room = starting_room
        self.current_room: Room = starting_room
        self.answer_graph: Dict[enumerate: Dict[str, enumerate]] = {}
        self.graph: Dict[enumerate: Dict[str, enumerate]] = {}
        self.path = []
        self.rooms = rooms
        self.current_path = []
        self.room_during_retravel = None
        self.dead_end_root_rooms: Dict[enumerate: Room] = {}
        self.dead_end_nodes: Dict[enumerate: Room] = {}

    def travel_long(self, directions: List):
        for direction in directions:
            self.travel(direction)

    def travel(self, direction, hide_error = True, show_rooms = True):
        next_room = self.current_room.get_and_remove_room_in_direction(
            direction, hide_error)
        if next_room is not None:
            self.path.append(direction)
            self.check_in_graph(next_room)
            if (show_rooms):
                print(
                    f"Moving {direction} {self.current_room.id} -> {next_room.id} ")
            self.current_room = next_room
        else:
            print("You cannot move in that direction.")
            return False

    def start(self):
        self.find_dead_ends(self.current_room)
        print(f"We have found {len(self.dead_end_root_rooms)} dead root rooms.")
        print(f"There are {len(self.dead_end_nodes)} dead end nodes")
        if self.current_room.is_dead_end_node:
            self.traverse_dead_end()
        print("What do I do now.")
        while len(self.dead_end_root_rooms) > 0:
            self.find_nearest_root_room()
            self.traverse_dead_end()
        print("Finished traversing dead end nodes.")
        print(f'We have been to {len(self.graph)} new rooms.')
        print(f'We have moved {len(self.path)} times.')
        while len(self.graph) < self.rooms:
            self.bfs_for_next_room()
        print(f"We have found {len(self.graph)} rooms")
        return self.path.copy()



    def traverse_dead_end(self):
        print("Traversing dead end.")
        self.dead_end_root_rooms.pop(self.current_room.id)
        stack = Stack()
        while len(self.current_room.dead_end_out) > 0:
            (dir, room) = self.current_room.dead_end_out.popitem()
            stack.push((dir, room))
        while len(self.current_room.dead_end_in) > 0:
            (dir, room) = self.current_room.dead_end_in.popitem()
            stack.push((dir, room))


        while stack.size() > 0:
            (dir, room) = stack.pop()
            self.travel(dir, True)
            while len(room.dead_end_out) > 0:
                (new_dir, new_room) = room.dead_end_out.popitem()
                stack.push((new_dir, new_room))
            while len(room.dead_end_in) > 0:
                (new_dir, new_room) = room.dead_end_in.popitem()
                stack.push((new_dir, new_room))

        print("Finished with dead end.")

    def find_nearest_root_room(self):
        [nearest, path] = self.bft(self.current_room, self.nearest_root_room_call_back)
        self.travel_long(path[nearest.id])

    def nearest_root_room_call_back(self, room, results, paths):
        if room.id in self.dead_end_root_rooms.keys():
            return [True, room]
        return [False, None]

    def bft(self, start: Room, call_back):
        queue = Queue()
        queue.enqueue(start)
        results = {start.id: self.create_room_for_graph(start)}
        visited = set()
        paths = {}

        while queue.size() > 0:
            room: Room = queue.dequeue()

            if room.number_of_paths == 0:
                room.set_number_of_paths()

            if room.id not in visited:

                if call_back is not None:
                    [end, result] = call_back(room, results, paths)
                    if end:
                        if result is not None:
                            results = result
                        break

                visited.add(room.id)
                directions = room.get_exits()
                for direction in directions:
                    new_room = room.get_room_in_direction(direction)

                    if new_room.id not in results.keys():
                        results[new_room.id] = self.create_room_for_graph(
                            new_room)

                    if room.id in paths.keys():
                        paths[new_room.id] = paths[room.id] + [direction]
                    else:
                        paths[new_room.id] = [direction]

                    results[room.id][direction] = new_room.id

                    if new_room.id not in visited:
                        queue.enqueue(new_room)

        return [results, paths]

    def bfs_for_next_room(self):

        [results, paths] = self.bft(self.current_room, self.bfs_for_next_room_call_back)
        self.travel_long(paths[results.id])

    def bfs_for_next_room_call_back(self, room, results, paths):
        if room.id in paths.keys():
            direction = paths[room.id][-1:]
            if room.id not in self.graph.keys():
                return [True, room]

        return [False, None]

    def dft(self, start, call_back = None):
        stack = Stack()
        stack.push(start)
        results = {self.starting_room.id: self.create_room_for_graph(
            self.starting_room)}
        visited = set()
        paths = {}

        while stack.size() > 0:
            room: Room = stack.pop()

            if room.number_of_paths == 0:
                room.set_number_of_paths()

            if room.id not in visited:
                visited.add(room.id)
                directions = room.get_exits(False)

                if call_back is not None:
                    [end, result] = call_back(room, results, paths)
                    if end:
                        if result is not None:
                            results = result
                        break

                for dir in directions:
                    next_room: Room = room.get_room_in_direction(dir)

                    if next_room.id not in visited:
                        if room.id in paths.keys():
                            paths[next_room.id] = paths[room.id] + [dir]
                        else:
                            paths[next_room.id] = [dir]

                        if next_room.id not in results.keys():
                            results[room.id] = self.create_room_for_graph(room)

                        results[room.id][dir] = next_room.id
                        stack.push(next_room)

        return [results, paths]

    @staticmethod
    def create_room_for_graph(room):
        directions = room.get_exits()
        room_graph = {}
        for dir in directions:
            room_graph[dir] = "?"

        return room_graph

    def find_dead_ends(self, start):
        self.dft(self.starting_room, self.dead_end_dft_callback)

    def check_dead_ends_root_nodes(self):
        queue = Queue

        for room in self.dead_end_root_rooms.values():
            queue.enqueue(room)

        while queue.size() > 0:
            room = queue.dequeue()
            self.find_dead_end_start_room(room)

    def dead_end_dft_callback(self, room, results, paths):
        dead_end_routes = len(room.dead_end_in)
        if room.number_of_paths - dead_end_routes == 1:
            if room.id not in self.dead_end_nodes.keys():
                self.dead_end_nodes[room.id] = room

            root_room = self.find_dead_end_start_room(room)
            if root_room.id not in self.dead_end_root_rooms.keys():
                self.dead_end_root_rooms[root_room.id] = root_room
            if root_room.id in self.dead_end_nodes.keys():
                self.dead_end_nodes.pop(root_room.id)

        return [False, None]

    def find_dead_end_start_room(self, start: Room):

        queue = Queue()
        queue.enqueue(start)

        while queue.size() > 0:

            current_room: Room = queue.dequeue()
            dead_end_paths = len(current_room.dead_end_in)

            if current_room.number_of_paths - dead_end_paths > 2:
                return current_room

            directions = current_room.get_exits()

            for direction in directions:
                new_room: Room = current_room.get_room_in_direction(direction)

                if new_room.id in self.dead_end_nodes.keys():
                    continue

                dead_end_paths = len(new_room.dead_end_in)
                if new_room.number_of_paths - dead_end_paths > 2:
                    new_room.is_dead_end_root_node = True
                    new_room.set_dead_end_in_node(current_room, direction)
                    if new_room.id in self.dead_end_nodes.keys():
                        self.dead_end_nodes.pop(new_room.id)
                    return new_room
                elif new_room.number_of_paths - dead_end_paths == 2:
                    new_room.is_dead_end_node = True
                    new_room.set_dead_end_in_node(current_room, direction)
                else:
                    if new_room.number_of_paths == 1:
                        new_room.dead_end = True

                if new_room.is_dead_end_root_node:
                    self.dead_end_root_rooms.pop(new_room.id)
                    new_room.is_dead_end_root_node = False

                if new_room.id not in self.dead_end_nodes.keys():
                    self.dead_end_nodes[new_room.id] = new_room

                queue.enqueue(new_room)

    def check_in_graph(self, room, print = False):
        if room.id in self.graph.keys():
            return
        else:
            self.graph[room.id] = room
            if print:
                print(f"Visited new room. ID: {room.id}")
                print(f'{len(self.graph)} found out of {self.rooms}.')
