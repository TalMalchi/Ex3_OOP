from unittest import TestCase
from src.DiGraph import DiGraph
from src.NodeData import NodeData


def createGraph():
    g = DiGraph()
    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_node(4)
    g.add_node(5)
    g.add_node(6)
    g.add_node(7)
    g.add_node(8)
    g.add_node(9)
    g.add_node(10)
    g.add_edge(1, 2, 1)
    g.add_edge(1, 3, 2)
    g.add_edge(3, 2, 1)
    g.add_edge(0, 2, 1)
    g.add_edge(0, 4, 1)
    g.add_edge(4, 5, 1)
    g.add_edge(5, 6, 1)
    g.add_edge(7, 1, 1)
    g.add_edge(8, 0, 1)
    g.add_edge(9, 5, 1)
    g.add_edge(6, 9, 1)
    g.add_edge(9, 4, 1)
    g.add_edge(4, 8, 1)
    g.add_edge(3, 7, 1)
    g.add_edge(2, 1, 1)
    g.add_edge(3, 6, 1)
    g.add_edge(10, 6, 1)

    return g


class Test(TestCase):
    # def test_di_graph(self):
    #     self.fail()

    def test_getNode(self):
        gr = createGraph()
        self.assertEqual(0, gr.getNode(0).get_id())

    def test_v_size(self):
        gr= createGraph()
        size=gr.v_size()
        self.assertEqual(11, size)

    def test_e_size(self):
        gr= createGraph()
        self.assertEqual(17, gr.e_size())

    def test_get_all_v(self):
        gr= createGraph()
        v = gr.get_all_v()
        self.assertEqual(11, v.__len__ ())

    def test_all_in_edges_of_node(self):
        gr= createGraph()
        size = gr.all_in_edges_of_node(2)
        self.assertEqual(3, size.__len__())
        gr.remove_edge(0 ,2)
        size2 = gr.all_in_edges_of_node(2)
        self.assertEqual(2, size2.__len__())

    def test_all_out_edges_of_node(self):
        gr= createGraph()
        size = gr.all_out_edges_of_node(9)
        self.assertEqual(2, size.__len__())
        gr.add_edge(9 ,2 ,10)
        size2 = gr.all_out_edges_of_node(9)
        self.assertEqual(3, size2.__len__())

    def test_add_node(self):
        gr=createGraph()
        gr.add_node(2) #exsit node
        gr.add_node(11)
        gr.add_node(12)
        gr.add_node(12) #add the same node twice
        self.assertEqual(13, gr.v_size())

    def test_add_edge(self):
        gr = createGraph()
        gr.add_edge(2, 9, 6)
        gr.add_edge(9, 0, 6)
        self.assertEqual(19, gr.e_size())
        size_out = gr.all_out_edges_of_node(9)
        self.assertEqual(3, size_out.__len__())
        size_in = gr.all_in_edges_of_node(9)
        self.assertEqual(2, size_in.__len__())


    def test_remove_edge(self):
        gr = createGraph()
        gr.remove_edge(3,2)
        gr.remove_edge(1,3)
        self.assertEqual(15, gr.e_size())
        size_out = gr.all_out_edges_of_node(3)
        self.assertEqual(2, size_out.__len__())
        size_in = gr.all_in_edges_of_node(3)
        self.assertEqual(0, size_in.__len__())

    def test_remove_node(self):
        gr = createGraph()
        gr.remove_node(10)
        self.assertEqual(10, gr.v_size())
        self.assertEqual(16, gr.e_size())
        gr.remove_node(8)
        self.assertEqual(14, gr.e_size())














