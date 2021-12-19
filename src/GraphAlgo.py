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
        pass

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass

    def plot_graph(self) -> None:
        pass

    def get_graph(self) -> GraphInterface:
        return self.g

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        super().TSP(node_lst)

    def centerPoint(self) -> (int, float):
        super().centerPoint()
