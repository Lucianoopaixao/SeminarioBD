import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

class Neo4jConnection:
    def __init__(self):
        # Pega os dados do .env ao instanciar a classe
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USER")
        pwd = os.getenv("NEO4J_PASSWORD")
        
        # Cria a conexão
        self.driver = GraphDatabase.driver(uri, auth=(user, pwd))

    def close(self):
        # Fecha a conexão para não consumir memória desnecessária
        if self.driver:
            self.driver.close()

    def get_driver(self):
        return self.driver