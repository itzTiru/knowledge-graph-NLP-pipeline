import networkx as nx
from ..graph.neo4j_client import Neo4jClient

class GraphReasoner:
    def __init__(self):
        self.client = Neo4jClient()
        self.nx_graph = nx.DiGraph()

    def load_graph_from_neo4j(self):
        query = "MATCH (n)-[r]->(m) RETURN n.name AS source, type(r) AS relation, m.name AS target"
        results = self.client.execute_query(query)
        
        self.nx_graph.clear()
        for record in results:
            self.nx_graph.add_edge(record['source'], record['target'], relation=record['relation'])
            
        print(f"Loaded graph into NetworkX: {self.nx_graph.number_of_nodes()} nodes, {self.nx_graph.number_of_edges()} edges.")

    def calculate_centrality(self):
        if self.nx_graph.number_of_nodes() == 0:
            print("Graph is empty. Load from Neo4j first.")
            return {}
            
        centrality = nx.degree_centrality(self.nx_graph)
        sorted_centrality = sorted(centrality.items(), key=lambda item: item[1], reverse=True)
        return sorted_centrality

    def find_shortest_path(self, source, target):
        try:
            path = nx.shortest_path(self.nx_graph, source=source, target=target)
            return path
        except nx.NetworkXNoPath:
            return None
        except nx.NodeNotFound:
            return None

    def close(self):
        self.client.close()
