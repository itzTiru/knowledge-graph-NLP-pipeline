from neo4j import GraphDatabase
import os


class Neo4jClient:
    def __init__(self):

        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "password")
        
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.verify_connection()
        except Exception as e:
            print(f"Failed 4j driver: {e}")
            raise

    def close(self):
        self.driver.close()

    def verify_connection(self):
        with self.driver.session() as session:
            result = session.run("RETURN 1 AS num")
            print(f"Neo4j connection posit. {result.single()['num']}")

    def execute_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]
