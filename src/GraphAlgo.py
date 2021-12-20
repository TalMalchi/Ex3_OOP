import json
import sys
from typing import List
from GraphAlgoInterface import GraphAlgoInterface  # abstractmethod
from src import GraphInterface
from DiGraph import DiGraph
from queue import PriorityQueue
import heapq
import matplotlib.pyplot as plt

#{src: {dest: weight}}
"""@Override
    public NodeData center() {
        try {
            int minMaxKey = Integer.MAX_VALUE;
            double minMaxValue = Double.MAX_VALUE;

            Iterator<NodeData> itr = graph.nodeIter();
            while (itr.hasNext()) { //for each node
                NodeData currNode = itr.next();
                HashMap<Integer, double[]> map = this.DijkstrasAlgo(currNode);
                double currMaxVal = 0;
                for (Map.Entry<Integer, double[]> entry : map.entrySet()) { //for each entry in map
                    if (currMaxVal < entry.getValue()[0]) {
                        currMaxVal = entry.getValue()[0];
                    }
                }
                if (minMaxValue > currMaxVal) {
                    minMaxKey = currNode.getKey();
                    minMaxValue = currMaxVal;
                }
            }
            return this.graph.getNode(minMaxKey);
        }
        catch (Exception e) {
            return null;
        }
    }"""  # Center function on java


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

        # add edges to list
        edges = []
        for n in self.g.get_all_v().keys():
            for dest in self.g.all_out_edges_of_node(n):
                edges.append({"src": n, "dest": dest, "w": self.g.all_out_edges_of_node(n).get(dest)})

        # add nodes to list
        nodes = []
        for key in self.g.get_all_v().keys():
            nodes.append({"id": key, "pos": self.g.get_all_v()[key].get_pos()})

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

    def dijkstra(self, start):  # TODO
        """Taken and adapted from: https://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php"""
        # Set the distance for the start node to zero
        start.set_distance(0)

        # Put tuple pair into the priority queue
        unvisited_queue = [(v.get_distance(), v) for v in self.g]
        heapq.heapify(unvisited_queue)

        #Visited=[False for i in range(self.g)] #initialized boolean array for visit or not
        Visited={}
        for i in range (self.g.edge_size)
            Visited[]

        while len(unvisited_queue):
            uv = heapq.heappop(unvisited_queue)  # Pops a vertex with the smallest distance
            current = uv[1]
            #current.set_visited()
            #Visited[]

            for next_node in current.adjacent:  # for next in v.adjacent:
                if next_node.visited:  # if visited, skip
                    continue
                new_dist = current.get_distance() + current.get_weight(next_node)
                if new_dist < next_node.get_distance():
                    next_node.set_distance(new_dist)
                    next_node.set_previous(current)

            # Rebuild heap
            while len(unvisited_queue):  # Pop every item
                heapq.heappop(unvisited_queue)
            # Put all vertices not visited into the queue
            unvisited_queue = [(v.get_distance(), v) for v in self.g if not v.visited]
            heapq.heapify(unvisited_queue)

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass

    # def plot_graph(self) -> None:
        # Graph= nx.DiGraph()
        Gtemp = self.g
        # Graph = nx.Gtemp
        # nx.draw(Graph, with_labels=True)

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
