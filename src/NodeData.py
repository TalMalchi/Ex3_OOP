import sys


class NodeData:
    # static variables, for GUI
    min_value = {'x': -sys.maxsize, 'y': -sys.maxsize, 'z': -sys.maxsize}
    max_value = {'x': sys.maxsize, 'y': sys.maxsize, 'z': sys.maxsize}

    def __init__(self, pos: str, id: int):
        self.id = id
        if pos == 'None' or pos is None:
            self.x = None
            self.y = None
            self.z = None
        else:
            pos_lst = pos.split(',')
            self.x = float(pos_lst[0])
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

    def get_id(self) -> int:
        return self.id

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def get_pos(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z)

    def __str__(self):  # for debugging purposes only
        return str("id: " + str(self.id) + " pos: " + str(self.x) + ',' + str(self.y) + ',' + str(self.z))
