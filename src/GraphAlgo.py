import json
import sys
from typing import List

from GraphAlgoInterface import GraphAlgoInterface  # abstractmethod
from DiGraph import DiGraph
import heapq
from src.GUI.GraphGUI import GUI

# dijkstra returns: {node_id: [distance, previous_node_id]}

# {src: {dest: weight}}
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

    def dijkstra(self, start):
        """Taken and adapted from: https://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php"""
        final_dijkstra={} #define new dict
        # Set the distance for the start node to zero
        start.set_distance(0)

        # Put tuple pair into the priority queue
        unvisited_queue = [(node.get_distance(), node) for node in self.g.get_all_v()]
        heapq.heapify(unvisited_queue)

        # First ,we will initialized boolean array for visit or not
        Visited = {}  # {src: {dest: boolean}}
        for curr_src_key in self.Edges.keys():  # for each src key in the dictionary
            for innerKey in self.Edges[curr_src_key].keys():  # for each dest
                Visited.update({curr_src_key: {innerKey,False}})  # put all src&dest in new dictionary and update all values like this: {src: {dest: False}}
                # Visited.update({self.Edges[curr_src_key][innerKey]: False})  #weight
        ###FOR YUVAL DO NOT TOUCH
        # in_edges.update({curr_src_key: self.Edges[curr_src_key][id1]})
        # for key in self.Edges.keys(): src
        #     for innerkey in self.Edges[key].keys(): dest
        #         self.Edges[key][innerkey]  #weight

        while len(unvisited_queue):
            uv = heapq.heappop(unvisited_queue)  # Pops a vertex with the smallest distance
            current = uv[1]
            # we will change the edge as visited (means True)
            # Visited.update({current.src: {current.dest, True}})#################################
            current.set_visited()  # turn to true

            # now I would like to create one long dictionary of all neighbors of current node
            # means one long dictionary of all_in_edges_of_node and all_in_edges_of_node

            # All_neighbors_in=self.all_in_edges_of_node(current.id)
            All_neighbors = self.all_out_edges_of_node(current.id)

            # All_neighbors=All_neighbors_in.copy()# Copy the All_neighbors_in into the All_neighbors using copy() method
            # for key, value in All_neighbors.items():  # use for loop to iterate All_neighbors_out into the All_neighbors dictionary
            #     All_neighbors[key] = value

            for next_node_id in All_neighbors.keys():  # for next in All_neighbors:
                next_node = self.g.getNode(next_node_id)
                if next_node.get_visited():  # if visited, skip
                    continue
                new_dist = current.get_distance() + All_neighbors[next_node_id]  # {dest_node_id: edge_weight}
                if new_dist < next_node.get_distance():
                    next_node.set_distance(new_dist)
                    next_node.set_previous(current)
                    final_dijkstra.update({next_node.get_id():[next_node.get_distance(),next_node.get_previous.get_id()]})#update the relevant value in the answer

            # Rebuild heap
            while len(unvisited_queue):  # Pop every item
                heapq.heappop(unvisited_queue)
            # Put all vertices not visited into the queue
            unvisited_queue = [(v.get_distance(), v) for v in self.g if not v.visited]
            heapq.heapify(unvisited_queue)

        return final_dijkstra

        # dijkstra returns: {node_id: [distance, previous_node_id]}

    def TSP(self, node_lst: List[int]) -> (List[int], float):

        try:
            temp = []  # temp node list
            if len(node_lst) == 0:  # check if the node's list is empty
                return None
            currNode = node_lst[0]
            temp.append(currNode)
            visitedNodes = ()
            while len(node_lst) != 0:  # while there are still unvisited cities
                visitedNodes.add(currNode)  # add the current node to visitedNode list
                min_distance = sys.maxsize
                nextNode = currNode
                node_lst.remove(currNode)
                path = []  # init ans list of nodes
                for node in node_lst:  # go all over the unvisited nodes, calculate the closest one
                    if node not in visitedNodes:
                        curr_distance = self.shortest_path(currNode.get_id, node.get_id)[1]
                        if curr_distance < min_distance:
                            min_distance = curr_distance
                            nextNode = node
                            path = self.shortest_path(currNode.get_id, node.get_id)[
                                0]  # add the closest node to path list
                for node in path:  # The closest node's path (out of all cities) is appended to the list which is to be returned
                    if node is not path[0]:
                        temp.add(node)
                        visitedNodes.add(node)
                        node_lst.remove(node)
            if len(temp) == 0:
                return None

            return temp
        except:
            print("Invalid graph for TSP on these cities!")
            return None


    # def shortest_path(self, id1: int, id2: int) -> (float, list):
        # def shortest_path(self, id1: int, id2: int) -> (float, list):
        #     ans = []
        #     if self.g is None or self.g.v_size() is 1 or self.g.v_size() is 0 or \
        #             self.g.getNode(id1) is None or self.g.getNode(id2) is None:  # check if there is no path
        #         return float('inf'), []
        #     if id1 == id2:
        #         # shortest_path_dist =0 #if the source is the dist , destination is 0
        #         # ans.append(self.g.getNode(id))
        #         return 0, [id1]
        #     else:
        #         u

    def plot_graph(self) -> None:
        gui = GUI(self.g)
        gui.init_gui()

