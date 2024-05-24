import networkx as nx
import matplotlib.pyplot as plt
import Point

class Graph:
    def __init__(self):
        self.g = nx.DiGraph()

    def add_vertex(self, name):
        last_vertex = None
        all_vertices = list(self.g.nodes)
        
        if len(all_vertices) > 0:
            last_vertex = all_vertices[-1]
        self.g.add_node(name)
        if last_vertex is not None:
            self.g.add_edge(last_vertex, name)

    def get_last_element(self, c):
        if len(c) > 0:
            return list(c)[-1]
        return None

    def add_edge(self, v1, v2):
        self.g.add_edge(v1, v2)

    def get_graph(self):
        return self.g

    def get_output(self):
        return str(self.g.edges)

    def draw_graph(self):
        plt.figure(figsize=(10, 10))
        pos = nx.spring_layout(self.g)
        nx.draw(self.g, pos, with_labels=True, node_size=5000, node_color="skyblue", font_size=20, font_color="black")
        plt.title("Graph Viewer")
        plt.show()

    def get_spanning_tree(self):
        mst = nx.minimum_spanning_tree(self.g.to_undirected())
        print(mst.edges)

# Usage example:
if __name__ == "__main__":
    graph = Graph()
    p1 = Point(1, 2)  # Assuming Point class is defined somewhere
    p2 = Point(3, 4)
    graph.add_vertex(p1)
    graph.add_vertex(p2)
    graph.add_edge(p1, p2)
    graph.draw_graph()
    graph.get_spanning_tree()
