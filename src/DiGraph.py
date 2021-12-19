from GraphInterface import GraphInterface
from src import NodeData
from src.EdgeData import EdgeData

"""The edges are to be saved as a dictionary of dictionaries,  where the index of the outer dictionary is the source
node ID and its value is a dictionary of destination nodes (ID: Node). The overall structure is {src: {dest: weight}}"""


class DiGraph(GraphInterface):

    def __init__(self, nodes_dict, edge_dict):
        # self.nodeSize = node_size TODO: unneeded attribute, verify
        self.mc = 0
        self.nodes_dict = nodes_dict
        self.edge_dict = edge_dict
        self.edge_size = 0
        for inner_edge_dict in edge_dict.values():  # counting the number of edges
            self.edge_size += len(inner_edge_dict)

    def __init__(self):
        self.edge_dict = {}
        self.nodes_dict = {}
        self.mc = 0

    def v_size(self) -> int:  # TODO: verify
        return len(self.nodes_dict)

    def get_all_v(self) -> dict:  # TODO: verify
        return self.Nodes_dic

    def all_in_edges_of_node(self, id1: int) -> dict:  # TODO: verify. Uncertain how correct this is. To check
        in_edges = {}
        for curr_src_key in self.edge_dict.keys():  # for each src key in the dictionary
            if id1 in self.edge_dict[curr_src_key]:  # if id1 is a valid destination node
                in_edges.update({curr_src_key, self.edge_dict[curr_src_key][id1]})
        return in_edges

    def all_out_edges_of_node(self, id1: int) -> dict:  # TODO: verify
        return self.edge_dict[id1]

    def e_size(self) -> int:  # TODO: verify
        return self.edge_size

    def get_mc(self) -> int:  # TODO: verify
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:  # TODO: verify
        if id1 in self.edge_dict and id2 in self.edge_dict[id1]:  # if edge exists (no matter its weight
            return False
        if id1 not in self.nodes_dict or id2 not in self.nodes_dict:  # if one of the nodes or both don't exist
            return False
        if id1 in self.edge_dict:  # source node dict exists
            self.edge_dict.get(id1).update({id2: weight})
        else:  # source node dict doesn't exists
            self.edge_dict.update({id1: {id2: weight}})
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:  # TODO: verify
        if node_id in self.nodes_dict:
            return False
        self.nodes_dict.update({node_id: pos})
        return True

    def remove_node(self, node_id: int) -> bool:  # TODO: verify
        if node_id not in self.nodes_dict:
            return False
        self.nodes_dict.pop(node_id)
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:  # TODO: verify
        if node_id1 not in self.edge_dict or node_id2 not in self.edge_dict[node_id1]:  # edge doesnt exist
            return False
        if len(self.edge_dict[node_id1]) == 1:  # only destination from current src node
            self.edge_dict.pop(node_id1)  # remove the src node itself
        else:
            self.edge_dict[node_id1].pop(node_id2)
        return True
