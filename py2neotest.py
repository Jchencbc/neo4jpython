import csv

from py2neo import *

graph = Graph("http://localhost:7474/browser/", username='neo4j', password='##12345')

# demo
person_demo = {"id": "1", "name": "张三", "age": "80", "company": "ABC公司", "sector": "互联网", "sex": "男",
               "disease": {"disease1": ['identity_id1', 'identity_id2', 'identity_id3'],
                           "disease2": ['identity_id1', 'identity_id2']}}
all_person_data = []
matcher = NodeMatcher(graph)


def up_node_logo(f):
    """读取标识节点数据存入数据库  单独维护"""
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        node_data = list(reader)
        # print(node_data[1)
    for i in range(0, len(node_data)):
        logo_node = Node('Identity', name=node_data[i][0], id=node_data[i][1], grade=node_data[i][2],
                         advice=node_data[i][3])
        graph.create(logo_node)


def up_node_person(info):
    """增加个人节点,建立节点联系  随时增加"""
    person_info = info
    person_node = Node('Person', name=person_info['name'], age=person_info['age'], sex=person_info['sex'],
                       sector=person_info['sector'], company=person_info['company'])
    graph.create(person_node)
    person_disease = info["disease"]
    for k, v in person_disease:
        disease_node = Node('Disease', name=k)
        person_own_disease = Relationship(person_node, 'own', disease_node)
        graph.create(disease_node)
        graph.create(person_own_disease)
        for i in v:
            identity_node = matcher.match('Identity', id=v).first()  # 查找当前疾病关联的标识
            disease_belong_identity = Relationship(disease_node, 'belong', identity_node)
            graph.create(disease_belong_identity)  # 构建疾病-标识关系


if __name__ == '__main__':
    pass
