from util import Stack, Queue
import random


class Player:
    def __init__(self, starting_room, rooms):
        self.starting_room = starting_room
        self.current_room = starting_room
        self.graph = {}
        self.path = []
        self.rooms = rooms
        self.moves_forward = 0
        self.moves_backward = 0
        self.current_path = []
        self.room_during_retravel = None
        self.dead_end_start_rooms = {}

    def travel_long(self, directioins):
        for direction in directioins:
            self.travel(direction)

    def travel(self, direction, log_error = True, show_rooms = False):
        next_room = self.current_room.get_and_remove_room_in_direction(
            direction, log_error)
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
        print(f"We have found {len(self.dead_end_start_rooms)} dead ends.")

        while len(self.graph) != self.rooms:
            room = self.dft(self.current_room, False)
            if len(room.path) == 0:
                self.dft(self.current_room, True)
                room = self.bfs_for_next_room(self.current_room)
                keys = self.dead_end_start_rooms.keys()
                self.travel_long(room.path)
                self.dft(self.current_room, True)
                continue
            else:
                next_move = random.choice(room.path[0])
                self.dft(self.current_room, True)
                room = self.current_room.get_room_in_direction(next_move)
                keys = self.dead_end_start_rooms.keys()
                if room.id in keys:
                    del (self.dead_end_start_rooms[room.id])
                    print("We are at a dead end thread.")
                    self.traverse_dead_end()
                else:
                    self.travel(next_move, False)

        return [i for i in self.path]

    def traverse_dead_end(self):
        print("Traversing dead end.")
        while self.current_room.dead_end_next:
            keys = self.dead_end_start_rooms.keys()
            if self.current_room.id in keys:
                del (self.dead_end_start_rooms[self.current_room.id])
            direction = self.current_room.dead_end_next_direction
            if direction is not None:
                self.current_room.dead_end_next_direction = None
                self.current_room.dead_end_next = None
                self.travel(direction, True, True)
            else:
                break

        print("Finished with dead end.")

    def bfs(self, start, end):
        queue = Queue()
        queue.enqueue(start)
        visited = set()

        while queue.size() > 0:
            room = queue.dequeue()
            if room.id not in visited:
                visited.add(room.id)
                directions = room.get_exits(False)
                for direction in directions:
                    new_room = room.get_room_in_direction(direction)
                    if new_room.id == end.id:
                        new_room.path = room.path + [direction]
                        return new_room
                    else:
                        if new_room.id not in visited:
                            new_room.path = room.path + [direction]
                            queue.enqueue(new_room)
        print("We didn't find a path to that room.")
        return False

    def bfs_for_next_room(self, start):
        queue = Queue()
        queue.enqueue(start)
        visited = set()

        while queue.size() > 0:
            room = queue.dequeue()
            if room.id not in visited:
                visited.add(room.id)
                directions = room.get_exits(False)
                for direction in directions:

                    new_room = room.get_room_in_direction(direction)
                    if len(new_room.unvisited_directions) > 0:
                        new_room.path = room.path + [direction]
                        return new_room
                    else:
                        if new_room.id not in visited:
                            new_room.path = room.path + [direction]
                            queue.enqueue(new_room)

        print("We didn't find a path to a new room.")
        return False

    def dft(self, start, reset):
        stack = Stack()
        stack.push(start)
        results = {}
        results[start.id] = start
        visited = set()

        while stack.size() > 0:
            room = stack.pop()
            if reset:
                room.path = []
                room.new_rooms = []

            if room.id not in visited:
                visited.add(room.id)
                directions = room.get_exits(False)
                for dir in directions:
                    next_room = room.get_room_in_direction(dir)
                    if next_room.id not in results.keys():
                        results[next_room.id] = next_room
                    if not reset:
                        if next_room.id not in self.graph.keys():
                            next_room.new_rooms = room.new_rooms + [
                                next_room.id]

                    if next_room.id not in visited:
                        next_room.path = room.path + [dir]
                        stack.push(next_room)

        # print("Graph reset")
        best = None
        for room in results.values():
            if best is None or len(best.new_rooms) < len(room.new_rooms):
                best = room

        return best

    def find_dead_ends(self, start):
        stack = Stack()
        stack.push(start)
        visited = set()

        while stack.size() > 0:
            room = stack.pop()
            if room.id not in visited:
                visited.add(room.id)
                directions = room.get_exits(False)
                if len(directions) == 1:
                    room.dead_end = True
                    self.find_dead_end_start_room(room)
                for direction in directions:
                    new_room = room.get_room_in_direction(direction)
                    if new_room.id not in visited:
                        stack.push(new_room)
        return

    def find_dead_end_start_room(self, start):
        queue = Queue()
        queue.enqueue(start)
        visited = []

        while queue.size() > 0:
            room = queue.dequeue()
            if room.id not in visited:
                visited.append(room.id)
                directions = room.get_exits(False)
                if len(directions) > 2:
                    self.dead_end_start_rooms[room.id] = room
                    room.is_dead_end_node = True
                    return
                else:
                    for direction in directions:
                        new_room = room.get_room_in_direction(direction)
                        if new_room.id not in visited:
                            new_room.set_dead_end_next(room, direction)
                            queue.enqueue(new_room)

    def check_in_graph(self, room, print = False):
        keys = self.graph.keys()
        if room.id in keys:
            return
        else:
            self.graph[room.id] = room
            if print:
                print(f"Visited new room. ID: {room.id}")
                print(f'{len(self.graph)} found out of {self.rooms}.')
