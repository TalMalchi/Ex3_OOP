from GraphInterface import GraphInterface


class DiGraph(GraphInterface) :

    def v_size(self) -> int:
        pass

    def get_all_v(self) -> dict:
        return super().get_all_v()

    def all_in_edges_of_node(self, id1: int) -> dict:
        return super().all_in_edges_of_node(id1)

    def all_out_edges_of_node(self, id1: int) -> dict:
        return super().all_out_edges_of_node(id1)

    def e_size(self) -> int:
        pass

    def get_mc(self) -> int:
        pass

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        pass

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        pass

    def remove_node(self, node_id: int) -> bool:
        pass

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        pass