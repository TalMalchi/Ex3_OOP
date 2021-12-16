import json
from typing import List
from GraphAlgoInterface import GraphAlgoInterface #abstractmethod
from src import GraphInterface
from EdgeData import  EdgeData
from NodeData import NodeData
from DiGraph import DiGraph


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph):
        self.g= g


    def load_from_json(self, file_name: str) -> bool:
        with open (file_name) as f:
            data= f.read()
            graph_algo= json.loads(data)
            for edge in graph_algo["Edges"]:
                self.g.Edge_dic.append(EdgeData(edge["src"], edge["w"], edge["dest"]))
            for node in graph_algo["Nodes"]:
                self.g.Nodes_dic.append(NodeData(node["pos"], node["id"]))


    def save_to_json(self, file_name: str) -> bool:
        pass

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass

    def plot_graph(self) -> None:
        pass

    def get_graph(self) -> GraphInterface:
        super().get_graph()

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        super().TSP(node_lst)

    def centerPoint(self) -> (int, float):
        super().centerPoint()