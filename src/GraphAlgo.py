import json
import os
import sys
from typing import List
from src.GraphAlgoInterface import GraphAlgoInterface
from src.DiGraph import DiGraph
import heapq
from src import GraphInterface


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph):
        self.g = g

    def get_graph(self) -> GraphInterface:
        return self.g

    def load_from_json(self, file_name: str) -> bool:
        try:
            self.g = DiGraph()
            root_dir = os.path.dirname(os.path.abspath(__file__))[:-4]
            path = os.path.join(root_dir, file_name)
            with open(path) as f:
                data = f.read()
                graph_algo = json.loads(data)
                for node in graph_algo["Nodes"]:
                    self.g.add_node(node["id"], node["pos"])
                for edge in graph_algo["Edges"]:
                    self.g.add_edge(edge["src"], edge["dest"], edge["w"])

        except IOError as e:
            print(e)
            return False
        return True

    def save_to_json(self, file_name: str) -> bool:
        try:
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

        except IOError as e:
            print(e)
            return False
        return True

    def dijkstra(self, start):
        """Taken and adapted from: https://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php"""
        for node in self.g.get_all_v().values():
            node.distance = sys.maxsize  # set distance to infinity for all nodes
            node.adjacent = {}  # {neighbor:weight}
            node.visited = False  # Mark all nodes as unvisited
            node.previous = None

        final_dijkstra = {}  # define new dict
        final_dijkstra.update({start.get_id(): [0, 0.5]})

        # Set the distance for the start node to zero
        start.set_distance(0)

        # Put tuple pair into the priority queue
        unvisited_queue = [(node.get_distance(), node) for node in self.g.get_all_v().values()]
        heapq.heapify(unvisited_queue)

        # First ,we will initialize boolean array for visit or not
        Visited = {}  # {src: {dest: boolean}}
        for curr_src_key in self.g.Edges.keys():  # for each src key in the dictionary
            for innerKey in self.g.Edges[curr_src_key].keys():  # for each dest
                # put all src&dest in new dictionary and update all values like this: {src: {dest: False}}
                Visited.update({curr_src_key: {innerKey, False}})

        while len(unvisited_queue):
            uv = heapq.heappop(unvisited_queue)  # Pops a vertex with the smallest distance
            current = uv[1]
            # we will change the edge as visited (means True)
            current.set_visited()  # turn to true

            # now I would like to create one long dictionary of all neighbors of current node
            All_neighbors = self.g.all_out_edges_of_node(current.id)
            for next_node_id in All_neighbors.keys():  # for next in All_neighbors:
                next_node = self.g.getNode(next_node_id)
                if next_node.get_visited():  # if visited, skip
                    continue
                new_dist = current.get_distance() + All_neighbors[next_node_id]  # {dest_node_id: edge_weight}
                if new_dist < next_node.get_distance():
                    next_node.set_distance(new_dist)
                    next_node.set_previous(current)
                    # update the relevant value in the answer means:{node_id: [distance, previous_node_id]}
                    final_dijkstra.update({next_node.get_id(): [next_node.get_distance(), next_node.get_previous(
                        current).get_id()]})

            # Rebuild heap
            while len(unvisited_queue):  # Pop every item
                heapq.heappop(unvisited_queue)
            # Put all vertices not visited into the queue
            unvisited_queue = [(v.get_distance(), v) for v in self.g.get_all_v().values() if not v.visited]

            heapq.heapify(unvisited_queue)

        return final_dijkstra

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        try:
            ans = []
            if self.g is None or self.g.getNode(id1) is None or self.g.getNode(
                    id2) is None:  # check if there is no path
                return float('inf'), []  # as requested
            if id1 == id2:
                return 0, [id1]  # if we get the sae node

            # dijkstra function return a dictionary with updated shortest path
            update_graph_dict = self.dijkstra(self.g.getNode(id1))
            if update_graph_dict[id2][0] == sys.maxsize:
                return float('inf'), []  # as requested

            curr_node_key = id2
            while curr_node_key != id1:  # go all over the dijkstra_dic
                ans.insert(0, curr_node_key)
                if update_graph_dict[curr_node_key][1] != 0.5:  # as we define before in dijkstra (the first element)
                    curr_node_key = update_graph_dict[curr_node_key][1]
                else:
                    break
            ans.insert(0, id1)  # add to the list all the nodes that append after id2
            return update_graph_dict[id2][0], ans
        except Exception:
            return float('inf'), []

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        temp = []  # temp node list
        if len(node_lst) == 0:  # check if the node's list is empty
            return None
        currNode = node_lst[0]
        temp.append(currNode)
        visitedNodes = []
        while len(node_lst) != 0:  # while there are still unvisited cities
            visitedNodes.append(currNode)  # add the current node to visitedNode list
            min_distance = sys.maxsize
            nextNode = currNode
            if currNode in node_lst:  # if currnode is in the node_lst we will remoove it
                node_lst.remove(currNode)
            path = []  # init ans list of nodes

            for node in node_lst:  # go all over the unvisited nodes, calculate the closest one
                if node not in visitedNodes:
                    # print(self.shortest_path(currNode, node)[1])
                    short_path_result = self.shortest_path(currNode, node)
                    curr_distance = short_path_result[0]
                    if curr_distance < min_distance:
                        min_distance = curr_distance
                        nextNode = node
                        path = short_path_result[1]  # add the closest node to path list
                        currNode = nextNode

            for node in path:  # The closest node's path (out of all cities) is appended to the list which is to be returned
                if node is not path[0]:  # add all vertices if they are not the first item in the 'path' list
                    temp.append(node)
                    visitedNodes.append(node)  # add node to visitednodes list
                    if node in node_lst:
                        node_lst.remove(node)
        if len(temp) == 0:
            return None
        # TODO: bug here, returned 1 temporarily
        return temp, 1

    def centerPoint(self) -> (int, float):
        dijk_route = {}  # note that we get from dijkstra : {node_id: [distance, previous_node_id]}
        try:
            minMaxKey = sys.maxsize
            minMaxValue = sys.maxsize

            for currNode in self.g.get_all_v().values():  # we will moove over all nodes in the graph
                dijk_route = self.dijkstra(currNode)
                currMaxVal = 0

                for value in dijk_route.values():  # for each value in the dictionary
                    currVal = value[0]  # we will take the distance as currVal
                    if currMaxVal < currVal:
                        currMaxVal = currVal
                if minMaxValue > currMaxVal:
                    minMaxKey = currNode.get_id()
                    minMaxValue = currMaxVal

            if minMaxValue == sys.maxsize:  # could be for example in case of empty graph
                return None

            return (minMaxKey, minMaxValue)

        except Exception:
            return None

    def plot_graph(self) -> None:
        from src.GUI.GraphGUI import GUI
        gui = GUI(self)
        gui.init_gui()
