from src.NodeData import NodeData
import unittest


class Test_NodeData(unittest.TestCase):
    def test_get_id(self):
        n1 = NodeData("1.15,1.1,2.2", 0)
        self.assertEqual(n1.get_id(), 0)

    def test_get_x(self):
        n1 = NodeData("1.15,1.1,2.2", 0)
        self.assertEqual(n1.get_x(),1.15)

    def test_get_y(self):
        n1 = NodeData("1.15,1.1,2.2", 0)
        self.assertEqual(n1.get_y(), 1.1)

    def test_get_z(self):
        n1 = NodeData("1.15,1.1,2.2", 0)
        self.assertEqual(n1.get_z(),2.2)

    def test_get_z(self):
        n1 = NodeData("1.15,1.1,2.2", 0)
        self.assertEqual(n1.get_pos(),"1.15,1.1,2.2")

    def test_set_get_prev(self):
        n1 = NodeData("1.15,1.1,2.2", 0)
        n2 = NodeData("1.3,2.1,7.6", 1)
        n1.set_previous(n2)
        self.assertEqual(n1.get_previous(n2).get_id(),n2.get_id())

    def test_set_get_dist(self):
        n1 = NodeData("1.15,1.1,2.2", 0)
        n1.set_distance(0)
        self.assertEqual(n1.get_distance(),0)
