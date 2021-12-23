from unittest import TestCase
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


def createGraph():
    g= DiGraph()
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
    g.add_edge(1,2,1)
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
    def test_get_graph_algo(self):
        self.fail()

    def test_load_from_json(self):
        g = DiGraph()
        g_algo = GraphAlgo(g)
        g_algo.load_from_json("G1.json")
        self.assertEqual(g_algo.g.getNode(0).get_x,35.19589389346247)
    def test_save_to_json(self): #done
        g = DiGraph()
        g_algo = GraphAlgo(g)
        g1 = DiGraph()
        g_algo1 = GraphAlgo(g)
        g_algo.save_to_json("check")
        g_algo1.load_from_json("check")
        #print(g_algo.g.v_size())
        #print(g_algo1.g.v_size())
        self.assertEqual(g_algo.g.v_size(),g_algo1.g.v_size())


    def test_shortest_(self):
            g = DiGraph()
            g_algo = GraphAlgo(g)
            g_algo.load_from_json("Test1.json");
            short_ans = g_algo.shortest_path(0, 3);#path does not exist
            self.assertEqual(0, len(short_ans[1]));
            self.assertEqual(float('inf'), short_ans[0]);

            g1 = DiGraph()
            g_algo1 = GraphAlgo(g1)
            g_algo1.load_from_json("G1.json");
            short_ans1 = g_algo1.shortest_path(0, 8);
            print(short_ans1)
            print(len(short_ans1[1]))
            self.assertEqual(6, len(short_ans1[1]));
            self.assertEqual(0, short_ans1[1][0]);
            self.assertEqual(1, short_ans1[1][1]);
            self.assertEqual(2, short_ans1[1][2]);
            self.assertEqual(6, short_ans1[1][3]);
            self.assertEqual(7, short_ans1[1][4]);
            self.assertEqual(8, short_ans1[1][5]);








