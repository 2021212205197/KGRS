import json
from py2neo import Graph
from django.conf import settings
from neo4j import GraphDatabase
import logging

logger = logging.getLogger(__name__)

class Neo4jDriver:
    def __init__(self):
        self._driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    def get_session(self):
        return self._driver.session()

driver = Neo4jDriver()

def process_neo4j_data(result, primary_label="TangDynasty"):
    """
    通用数据处理器：将neo4j结果转换为节点和关系
    """
    nodes = set()
    edges = []
    
    for record in result:
        logger.debug(f"Record: {record}")
        print(f"Record: {record}")
        
        source = record['n']
        source_id = source.get('id', 'Unknown')
        nodes.add(json.dumps(source, sort_keys=True))
        
        target = record['m']
        target_id = target.get('id', 'Unknown')
        nodes.add(json.dumps(target, sort_keys=True))
        
        relation = record['r']
        edges.append({
            'from': source_id,
            'to': target_id,
            'label': relation.get('type', 'Unknown'),
            'title': relation.get('detail', '')
        })
    
    logger.debug(f"Nodes: {nodes}")
    logger.debug(f"Edges: {edges}")
    print(f"Nodes: {nodes}")
    print(f"Edges: {edges}")
    
    return {
        'nodes': [json.loads(n) for n in nodes],
        'edges': edges
    }

def get_tang_graph_data(query, parameters=None):
    results = driver.get_session().run(query, parameters).data()
    return results