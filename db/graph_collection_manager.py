from . import Graph, NodeCollectionManager, Node
from utils.common import to_object_id
from utils.db_connector import *
from constants import NodeStatus


class GraphCollectionManager(object):
    """
    """

    node_collection_manager = NodeCollectionManager()

    @staticmethod
    def _update_node_statuses(db_graph):
        if not db_graph:
            return None
        node_ids = set(
            [to_object_id(node['parent_node']) for node in db_graph['nodes']]
            )
        db_nodes = GraphCollectionManager.node_collection_manager.get_db_nodes_by_ids(node_ids)

        node_id_to_db_node = {
            db_node['_id']: db_node for db_node in db_nodes
        }

        for g_node in db_graph['nodes']:
            id = to_object_id(g_node['parent_node'])
            if id in node_id_to_db_node:
                db_node = node_id_to_db_node[id]
                g_node['node_status'] = db_node['node_status']

        return db_graph

    @staticmethod
    def _transplant_node(node, new_node):
        if to_object_id(node.parent_node) == new_node._id:
            return node
        new_node.apply_properties(node)
        new_node.parent_node = str(new_node._id)
        new_node._id = node._id
        return new_node

    @staticmethod
    def update_blocks(graph):
        node_ids = set(
            [to_object_id(node.parent_node) for node in graph.nodes]
            )
        db_nodes = GraphCollectionManager.node_collection_manager.get_db_nodes_by_ids(node_ids)
        new_node_db_mapping = {}

        for db_node in db_nodes:
            original_parent_node_id = db_node['_id']
            new_db_node = db_node
            if original_parent_node_id not in new_node_db_mapping:
                while new_db_node['node_status'] != NodeStatus.READY and 'successor_node' in new_db_node and new_db_node['successor_node']:
                    n = GraphCollectionManager.node_collection_manager.get_db_node(new_db_node['successor_node'])
                    if n:
                        new_db_node = n
                    else:
                        break
                new_node_db_mapping[original_parent_node_id] = new_db_node

        new_nodes = [
            GraphCollectionManager._transplant_node(
                node,
                Node().load_from_dict(new_node_db_mapping[to_object_id(node.parent_node)])
            ) for node in graph.nodes]


        updated_nodes_count = sum(1
            for node, new_node in zip(graph.nodes, new_nodes) if node.parent_node != new_node.parent_node
        )

        graph.nodes = new_nodes
        return updated_nodes_count

    @staticmethod
    def get_graphs(graph_running_status):
        db_graphs = db.graphs.find({'graph_running_status': graph_running_status})
        graphs = []
        for db_graph in db_graphs:
            graphs.append(Graph())
            graphs[-1].load_from_dict(db_graph)
        return graphs

    @staticmethod
    def get_db_graphs(author, per_page=20, offset=0):
        db_graphs = db.graphs.find({
                '$or': [
                    {'author': author},
                    {'public': True}
                ]
                }).sort('insertion_date', -1).skip(offset).limit(per_page)
        return list(db_graphs)

    @staticmethod
    def get_db_graphs_count(author):
        return db.graphs.count({
                '$or': [
                    {'author': author},
                    {'public': True}
                ]
                })

    @staticmethod
    def get_db_graph(graph_id):
        return GraphCollectionManager._update_node_statuses(
            db.graphs.find_one({'_id': to_object_id(graph_id)})
            )
