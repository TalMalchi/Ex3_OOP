import json
import sys
from typing import List
from GraphAlgoInterface import GraphAlgoInterface  # abstractmethod
from src import GraphInterface
from DiGraph import DiGraph
import networkx as nx
from queue import PriorityQueue
import heapq
import matplotlib.pyplot as plt




class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph):
        self.g = g

    def load_from_json(self, file_name: str) -> bool:
        self.g = DiGraph()
        with open(file_name) as f:
            data = f.read()
            graph_algo = json.loads(data)
            for node in graph_algo["Nodes"]:
                self.g.add_node(node["id"], node["pos"])
            for edge in graph_algo["Edges"]:
                self.g.add_edge(edge["src"], edge["dest"], edge["w"])

    def save_to_json(self, file_name: str) -> bool:
        if self.g is None:
            return False
        edges = []
        for n in self.g.get_all_v().keys():
            for dest in self.g.all_out_edges_of_node(n):
                edges.append({"src": n, "dest": dest, "w": self.g.all_out_edges_of_node(n).get(dest)})

        nodes = []
        for key in self.g.get_all_v().keys():
            nodes.append({"id": key, "pos": self.g.get_all_v()[key]})

        saved_graph = {"Nodes": nodes, "Edges": edges}
        with open(file_name, 'w') as json_file:
            json.dump(saved_graph, json_file)

    # def dijkstras_algo(self, src_node: int) -> dict:
    #     map = {}
    #     visited = {}
    #     unvisited = {}
    #     map.update({src_node: [0, 0.5]})
    #     unvisited.update({src_node: None})
    #     for node in self.g.get_all_v().keys():
    #         if node != src_node:
    #             map.update({node: [sys.maxsize, 0.5]})
    #             unvisited.update({node, None})
    #
    #     curr_node = src_node
    #     curr_val = 0
    #     while not len(unvisited) == 0:
    #         neighbour_node_edges = self.g.all_out_edges_of_node(curr_node)
    #         for edge_dest in neighbour_node_edges.keys():
    #             if neighbour_node_edges[edge_dest] not in



    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass

    def plot_graph(self) -> None:
        # Graph= nx.DiGraph()
        Gtemp=self.g
        Graph=nx.Gtemp
        nx.draw(Graph, with_labels=True)

        # Graph=nx.DiGraph()
        # # Seed=13648
        # pos = nx.spring_layout(Graph)
        #
        # # AllNodes=self.g.get_all_v
        # # NodesLen=len(AllNodes)
        # # key_ofNodes=list(AllNodes) #create list of the keys.
        # # for node in AllNodes:         #now we will add the nodes
        # #     Graph.add_node(key_ofNodes[node])
        #
        # #define all data we neet to the plotting
        # NodesSize=len(self.g.get_all_v)
        # EdgesSize=self.g.edge_size
        # edge_colors = range(2,EdgesSize + 2)
        # edge_alphas = [(5 + i) / (EdgesSize + 4) for i in range(EdgesSize)]
        # nodes=nx.draw_networkx_nodes(Graph, pos, NodesSize,"indigo")
        # edges=nx.draw_networkx_edges(Graph, pos, NodesSize, "->", 10)
        # cmap = plt.cm.plasma
        #
        # for i in range(EdgesSize):
        #     edges[i].set_alpha(edge_alphas[i])
        # pc = plt.collections.PatchCollection(edges, cmap)
        # pc.set_array(edge_colors)
        # plt.colorbar(pc)
        #
        # ax = plt.gca()
        # ax.set_axis_off()
        # plt.show()
        #

        # nx.draw(Graph , with_labels = True)
        # plt.draw()
        # plt.show()

    def get_graph(self) -> GraphInterface:
        return self.g

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        super().TSP(node_lst)

    def centerPoint(self) -> (int, float):
        super().centerPoint()
