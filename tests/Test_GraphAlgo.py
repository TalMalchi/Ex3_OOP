from unittest import TestCase
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


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


class Test(TestCase):

    def test_load_from_json(self):
        g = DiGraph()
        g_algo = GraphAlgo(g)
        g_algo.load_from_json("data/G1.json")
        self.assertEqual(g_algo.g.getNode(0).get_x(), 35.19589389346247)

    def test_save_to_json(self):
        g = DiGraph()
        g_algo = GraphAlgo(g)
        g1 = DiGraph()
        g_algo1 = GraphAlgo(g)
        g_algo.save_to_json("out/check")
        g_algo1.load_from_json("out/check")
        self.assertEqual(g_algo.g.v_size(), g_algo1.g.v_size())

    def test_shortest_path(self):
        g = DiGraph()
        g_algo = GraphAlgo(g)
        g_algo.load_from_json("data/Test1.json")
        short_ans = g_algo.shortest_path(0, 3)  # path does not exist

        self.assertEqual(3, len(short_ans[1]))
        self.assertEqual(0, short_ans[1][0])
        self.assertEqual(1, short_ans[1][1])
        self.assertEqual(3, short_ans[1][2])

        g1 = DiGraph()
        g_algo1 = GraphAlgo(g1)
        g_algo1.load_from_json("data/G1.json")
        short_ans1 = g_algo1.shortest_path(0, 8)
        print(short_ans1)
        print(len(short_ans1[1]))
        self.assertEqual(6, len(short_ans1[1]))
        self.assertEqual(0, short_ans1[1][0])
        self.assertEqual(1, short_ans1[1][1])
        self.assertEqual(2, short_ans1[1][2])
        self.assertEqual(6, short_ans1[1][3])
        self.assertEqual(7, short_ans1[1][4])
        self.assertEqual(8, short_ans1[1][5])

        g2 = DiGraph()
        g_algo2 = GraphAlgo(g2)
        g_algo2.load_from_json("data/Test2.json")
        lst4 = g_algo2.shortest_path(4, 0)
        self.assertEqual(4, len(lst4[1]))

        self.assertEqual(4, lst4[1][0])
        self.assertEqual(3, lst4[1][1])
        self.assertEqual(1, lst4[1][2])
        self.assertEqual(0, lst4[1][3])

        g3 = DiGraph()
        g_algo3 = GraphAlgo(g3)
        g_algo3.load_from_json("data/G1.json")
        lst1 = g_algo3.shortest_path(2, 5)
        self.assertEqual(3, len(lst1[1]))

        self.assertEqual(2, lst1[1][0])
        self.assertEqual(6, lst1[1][1])
        self.assertEqual(5, lst1[1][2])

        g4 = DiGraph()
        g_algo4 = GraphAlgo(g4)
        g_algo4.load_from_json("data/emptyGraph.json")
        lst2 = g_algo4.shortest_path(0, 6)
        self.assertEqual(float('inf'), lst2[0])
        self.assertEqual(0, len(lst2[1]))  # the len should be 0

    def test_get_graph(self):
        g2 = DiGraph()
        g_algo2 = GraphAlgo(g2)
        g_algo2.load_from_json("data/A1.json")
        self.assertEqual(g_algo2.get_graph().getNode(0).get_id(), 0)

    def test_TSP(self):
        g = DiGraph()
        g_algo = GraphAlgo(g)
        g_algo.load_from_json("data/Test2.json")
        lstTest = []
        lstTest.append(g_algo.get_graph().getNode(4))
        lstTest.append(g_algo.get_graph().getNode(2))

        g1 = DiGraph()
        g_algo1 = GraphAlgo(g1)
        g_algo1.load_from_json("data/G1.json")

        lstTest = []
        lstTest.append(2)
        lstTest.append(5)
        lstTest.append(9)
        list = g_algo1.TSP(lstTest)  #####g_algo?

        self.assertEqual(2, list[0])
        self.assertEqual(6, list[1])
        self.assertEqual(5, list[2])
        self.assertEqual(6, list[3])
        self.assertEqual(7, list[4])
        self.assertEqual(8, list[5])
        self.assertEqual(9, list[6])

        g4 = DiGraph()
        g_algo4 = GraphAlgo(g4)
        g_algo4.load_from_json("data/emptyGraph.json")
        ans = g_algo4.TSP(lstTest)
        self.assertTrue(ans is None)#the graph is empty so function return none


    def test_center(self):
        g = DiGraph()
        g_algo = GraphAlgo(g)
        g_algo.load_from_json("data/G1.json")
        ans = g_algo.centerPoint()
        self.assertEqual(8, ans[0])

        g2 = DiGraph()
        g_algo2 = GraphAlgo(g2)
        g_algo2.load_from_json("data/Test2.json")
        self.assertEqual(3, g_algo2.centerPoint()[0])

        g3 = DiGraph()
        g_algo3 = GraphAlgo(g3)
        g_algo3.load_from_json("data/emptyGraph.json")
        temp = g_algo3.centerPoint()  # [0]
        self.assertTrue(temp is None)

    # BIG GRAPH DO NOT RUN
    # g4 = DiGraph()
    # g_algo4 = GraphAlgo(g4)
    # g_algo4.load_from_json("data/1000Nodes.json")
    # self.assertEqual(362, g_algo4.center()[0])

