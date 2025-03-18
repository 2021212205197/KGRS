import json
from py2neo import Graph
from django.conf import settings
from neo4j import GraphDatabase

class Neo4jDriver:
    def __init__(self):
        self._driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "wzk030424")
        )

    def get_session(self):
        return self._driver.session()

driver = Neo4jDriver()

# 新增通用处理函数
def process_neo4j_data(result, primary_label="TangDynasty"):
    """
    通用数据处理器：将neo4j结果转换为节点和关系
    """
    nodes = set()
    links = []
    
    for record in result:
        # 处理源节点
        source = {k.split('.')[1]: v for k, v in record.items() if k.startswith('n.')}
        nodes.add(json.dumps(source, sort_keys=True))
        
        # 处理目标节点
        target = {k.split('.')[1]: v for k, v in record.items() if k.startswith('m.')}
        nodes.add(json.dumps(target, sort_keys=True))
        
        # 处理关系
        links.append({
            'source': source.get('id', source['name']),
            'target': target.get('id', target['name']),
            'type': record['r.type'],
            'detail': record.get('r.detail', '')
        })
    
    return {
        'nodes': [json.loads(n) for n in nodes],
        'links': links
    }

# 新增唐朝专用连接器
def get_tang_graph():
    return Graph(
        settings.NEO4J_CONFIG['URI'],
        auth=(
            settings.NEO4J_CONFIG['USER'],
            settings.NEO4J_CONFIG['PASSWORD']
        )
    )

# CSV导入方法
def import_from_csv():
    with driver.get_session() as session:
        session.run("""
        LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
        MERGE (p:Person {id: row.id})
        SET p.name = row.name,
            p.title = row.title,
            p.birth = toInteger(row.birth)
        """)