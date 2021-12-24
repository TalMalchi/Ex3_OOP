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
        print(list[1])
        self.assertEqual(2, list[0][0])
        self.assertEqual(6, list[0][1])
        self.assertEqual(5, list[0][2])
        self.assertEqual(6, list[0][3])
        self.assertEqual(7, list[0][4])
        self.assertEqual(8, list[0][5])
        self.assertEqual(9, list[0][6])

        g4 = DiGraph()
        g_algo4 = GraphAlgo(g4)
        g_algo4.load_from_json("data/emptyGraph.json")
        ans = g_algo4.TSP(lstTest)
        self.assertTrue(ans is None)  # the graph is empty so function return none

    def test_center(self):
        """Results for center ->
A0 - (7, 6.806805834715163)
A1 - (8, 9.925289024973141)
A2 - (0, 7.819910602212574)
A3 - (2, 8.182236568942237)
A4 - (6, 8.071366078651435)
A5- (40, 9.291743173960954)"""
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
        temp = g_algo3.centerPoint()
        self.assertTrue(temp is None)

        g4 = DiGraph()
        g_algo4 = GraphAlgo(g4)
        g_algo4.load_from_json("data/A0.json")
        ans = g_algo4.centerPoint()[0]
        ans1 = g_algo4.centerPoint()[1]
        self.assertEqual(7, ans)
        self.assertEqual(6.806805834715163, ans1)

        g5 = DiGraph()
        g_algo5 = GraphAlgo(g5)
        g_algo5.load_from_json("data/A1.json")
        ans = g_algo5.centerPoint()[0]
        ans1 = g_algo5.centerPoint()[1]
        self.assertEqual(8, ans)
        self.assertEqual(9.925289024973141, ans1)

        g6 = DiGraph()
        g_algo6 = GraphAlgo(g6)
        g_algo6.load_from_json("data/A2.json")
        ans = g_algo6.centerPoint()[0]
        ans1 = g_algo6.centerPoint()[1]
        self.assertEqual(0, ans)
        self.assertEqual(7.819910602212574, ans1)

        g7 = DiGraph()
        g_algo7 = GraphAlgo(g7)
        g_algo7.load_from_json("data/A3.json")
        ans = g_algo7.centerPoint()[0]
        ans1 = g_algo7.centerPoint()[1]
        self.assertEqual(2, ans)
        self.assertEqual(8.182236568942237, ans1)

        g8 = DiGraph()
        g_algo8 = GraphAlgo(g8)
        g_algo8.load_from_json("data/A4.json")
        ans = g_algo8.centerPoint()[0]
        ans1 = g_algo8.centerPoint()[1]
        self.assertEqual(6, ans)
        self.assertEqual(8.071366078651435, ans1)

        g9 = DiGraph()
        g_algo9 = GraphAlgo(g9)
        g_algo9.load_from_json("data/A5.json")
        ans = g_algo9.centerPoint()[0]
        ans1 = g_algo9.centerPoint()[1]
        self.assertEqual(40, ans)
        self.assertEqual(9.291743173960954, ans1)

    # BIG GRAPH
    def test_big(self):
        g = DiGraph()
        g_algo = GraphAlgo(g)
        g_algo.load_from_json("data/100000.json")
        # g_algo.save_to_json("data/A5_saved.json")
        # result1, result2 = g_algo.centerPoint()
        # result1, result2 = g_algo.shortest_path(31, 826)
        result1, result2 = g_algo.TSP([1, 10, 11, 20, 13])
        print("\n" + str(result1), str(result2))
