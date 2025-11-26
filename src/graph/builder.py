from .neo4j_client import Neo4jClient

class GraphBuilder:
    def __init__(self):
        self.client = Neo4jClient()

    def clear_graph(self):
        query = "MATCH (n) DETACH DELETE n"
        self.client.execute_query(query)
        print("Graph cleared.")

    def create_graph(self, entities, relations):
        for ent in entities:

            label = ent['entity_group']
            name = ent['word']
            
            query = (
                f"MERGE (n:{label} {{name: $name}}) "
                "RETURN n"
            )
            self.client.execute_query(query, {"name": name})

        for ent1, rel, ent2 in relations:
            rel_type = rel.replace(" ", "_").upper()
            
            query = (
                "MATCH (a {name: $name1}), (b {name: $name2}) "
                f"MERGE (a)-[r:{rel_type}]->(b) "
                "RETURN type(r)"
            )
            self.client.execute_query(query, {"name1": ent1, "name2": ent2})
            
        print(f"Created {len(entities)} nodes and {len(relations)} relationships.")

    def close(self):
        self.client.close()
