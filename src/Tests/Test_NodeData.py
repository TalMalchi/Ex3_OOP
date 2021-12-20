from src.NodeData import NodeData
import unittest


class Test_NodeData(unittest.TestCase):
    def test_node_data(self):
        n1 = NodeData("1.15,1.1,2.2", 0)
        self.assertEqual(n1.get_pos(), "1.15,1.1,2.2")
        self.assertEqual(n1.get_id(), 0)
        self.assertEqual(n1.x, 1.15)
        self.assertEqual(n1.y, 1.1)
        self.assertEqual(n1.z, 2.2)
