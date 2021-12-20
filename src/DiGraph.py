import json

from GraphInterface import GraphInterface
from src.NodeData import NodeData
from src.EdgeData import EdgeData

"""The edges are to be saved as a dictionary of dictionaries,  where the index of the outer dictionary is the source
node ID and its value is a dictionary of destination nodes (ID: Node). The overall structure is {src: {dest: weight}}
Node format is {Node_id: NodeData}"""


class DiGraph(GraphInterface):

    def __init__(self, Nodes, Edges):
        self.mc = 0
        self.Nodes = Nodes
        self.Edges = Edges
        self.edge_size = 0
        for inner_Edges in Edges.values():  # counting the number of edges
            self.edge_size += len(inner_Edges)

    def __init__(self):
        self.Edges = {}
        self.Nodes = {}
        self.edge_size = 0
        self.mc = 0

    def v_size(self) -> int:
        return len(self.Nodes)

    def get_all_v(self) -> dict:
        return self.Nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        in_edges = {}
        for curr_src_key in self.Edges.keys():  # for each src key in the dictionary
            if id1 in self.Edges[curr_src_key]:  # if id1 is a valid destination node
                in_edges.update({curr_src_key: self.Edges[curr_src_key][id1]})
        return in_edges

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.Edges[id1]

    def e_size(self) -> int:
        return self.edge_size

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self.Nodes or id2 not in self.Nodes:  # if one of the nodes or both don't exist
            return False
        if id1 in self.Edges and id2 in self.Edges[id1]:  # if edge exists (no matter its weight)
            return False
        if id1 in self.Edges:  # source node dict exists
            self.Edges.get(id1).update({id2: weight})
        else:  # source node dict doesn't exists
            self.Edges.update({id1: {id2: weight}})
        self.edge_size += 1
        self.mc += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self.Nodes:
            return False
        temp = NodeData(pos, node_id)
        self.Nodes.update({node_id: temp})
        self.mc += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self.Nodes:
            return False

        if node_id in self.Edges.keys():
            self.Edges.pop(node_id)  # remove edges FROM node_id
        for curr_src in self.Edges.keys:
            self.remove_edge(curr_src, node_id)  # remove edges TO node_id
        self.Nodes.pop(node_id)  # remove node
        self.mc += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self.Edges and node_id2 not in self.Edges[node_id1]:  # edge doesnt exist
            return False
        if len(self.Edges[node_id1]) == 1:  # only destination from current src node
            self.Edges.pop(node_id1)  # remove the src node itself
        else:
            self.Edges[node_id1].pop(node_id2)
        self.edge_size -= 1
        self.mc += 1
        return True

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
