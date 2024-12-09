
class MermaidNode:
    _default_id_template = 'Node{ID}'
    _current_id = 0  # Class attribute to keep track of the next ID

    def __init__(self, node_caption: str, node_id: str = None, id_is_caption=True):
        MermaidNode._current_id += 1
        if id_is_caption:
            self.node_id = node_caption
        else:
            self.node_id = node_id or self._default_id_template.format(ID=MermaidNode._current_id)
        self.node_caption = node_caption


class MermaidEdge:
    def __init__(self, src_node_id: str, dst_node_id: str, edge_caption: str = None):
        self.src_node_id = src_node_id
        self.dst_node_id = dst_node_id
        self.edge_caption = edge_caption


class MermaidDiagram:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node_caption: str, node_id: str = None, id_is_caption=True):
        same_node = [x for x in self.nodes if x.node_caption == node_caption or x.node_id == node_id]
        if same_node:
            return same_node[0].node_id
        mn = MermaidNode(node_caption, node_id, id_is_caption)
        self.nodes.append(mn)
        return mn.node_id

    def add_node_with_edge(self, node_caption: str, node_id: str = None, edge_caption: str = None,
                           id_is_caption=True, new_node_is_source=True):
        new_node_id = self.add_node(node_caption=node_caption, id_is_caption=id_is_caption)
        src_node_id, trg_node_id = (new_node_id, node_id) if new_node_is_source else (node_id, new_node_id)
        self.add_edge(target=trg_node_id, source=src_node_id, caption=edge_caption)
        return new_node_id

    def add_source_node(self, node_caption: str, node_id: str = None, edge_caption: str = None):
        return self.add_node_with_edge(node_caption=node_caption, node_id=node_id, edge_caption=edge_caption,
                                       id_is_caption=False, new_node_is_source=True)

    def add_edge(self, source: str, target: str, caption: str = None):
        self.edges.append(MermaidEdge(source, target, caption))

    def generate_mermaid_code(self):
        mermaid_code = "flowchart TD;\n"
        for node in self.nodes:
            mermaid_code += f"    {node.node_id}[{node.node_caption}];\n"
        for edge in self.edges:
            ec = f'|{edge.edge_caption}|' if edge.edge_caption else '' 
            mermaid_code += f"    {edge.src_node_id}-->{ec}{edge.dst_node_id};\n"
        return mermaid_code
