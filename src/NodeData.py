import sys


class NodeData:
    # static variables, for GUI
    min_value = {'x': -sys.maxsize, 'y': -sys.maxsize, 'z': -sys.maxsize}
    max_value = {'x': sys.maxsize, 'y': sys.maxsize, 'z': sys.maxsize}

    def __init__(self, pos: str, id: int):
        self.id = id
        if pos == 'None' or pos is None: #if pos is nonwwe will initilized all x,y,z values as none
            self.x = None
            self.y = None
            self.z = None
        else:
            pos_lst = pos.split(',') #split string by ,
            self.x = float(pos_lst[0]) #we will take the
            self.y = float(pos_lst[1])
            self.z = float(pos_lst[2])
            if NodeData.min_value['x'] < self.x:
                NodeData.min_value['x'] = self.x
            if NodeData.min_value['y'] < self.y:
                NodeData.min_value['y'] = self.y
            if NodeData.min_value['z'] < self.z:
                NodeData.min_value['z'] = self.z

            if NodeData.max_value['x'] > self.x:
                NodeData.max_value['x'] = self.x
            if NodeData.max_value['y'] > self.y:
                NodeData.max_value['y'] = self.y
            if NodeData.max_value['z'] > self.z:
                NodeData.max_value['z'] = self.z

        self.distance = sys.maxsize  # set distance to infinity for all nodes
        self.adjacent = {}  # {neighbor:weight}
        self.visited = False  # Mark all nodes as unvisited
        self.previous = None

    def get_visited(self):
        return self.visited

    def get_id(self) -> int:
        return self.id

    def get_distance(self):
        return self.distance

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def get_pos(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z)

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_previous(self, prev):
        self.previous = prev

    def set_distance(self, dist):
        self.distance = dist

    def get_previous(self, current):
        return self.previous

    def __str__(self):  # for debugging purposes only
        return str("id: " + str(self.id) + " pos: " + str(self.x) + ',' + str(self.y) + ',' + str(self.z))

    def set_visited(self):
        self.visited = True

#for using heapq.heapify in GraphAlgo

    def __eq__(self, other):
        return self.get_id() == other.get_id

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __le__(self, other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)