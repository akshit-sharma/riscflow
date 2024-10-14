import graphviz


class ControlFlowGraph:
    """Represents the control flow graph."""

    def __init__(self):
        self.nodes = []  # List of CFGNodes
        self.label_map = {}  # Maps labels to CFGNodes for easy linking
        self.start_node = None  # Reference to the start node

    def __setitem__(self, label, node):
        """Add a new node to the CFG using the [] operator."""
        if not self.nodes:
            # The first node added is the start node
            self.start_node = node
            node.is_start = True

        # Add the node to the list of nodes
        self.nodes.append(node)

        # Map the label to the node for future reference
        if label:
            self.label_map[label] = node

    def __getitem__(self, label):
        """Retrieve a node by its label using the [] operator."""
        return self.label_map.get(label, None)

    def __contains__(self, label):
        """Check if a node with the given label exists in the CFG."""
        return label in self.label_map

    def add_edge(self, from_node, to_node, condition=None):
        """Create a control flow edge between two nodes."""
        from_node.add_successor(to_node, condition)

    def to_graphviz(self, nodes):
        """Generate a Graphviz Digraph for the control flow graph."""
        dot = graphviz.Digraph(format="svg")

        # Add nodes with the instructions as part of the label
        for node in nodes:
            label_text = f"{node.label if node.label else 'Unnamed Block'}\n"
            for ast_node in node.ast_nodes:
                label_text += f"{ast_node}\n"

            # Customize the appearance of start and exit nodes
            node_shape = 'ellipse'
            if node.is_macro:
                node_shape = 'parallelogram'
            elif node.is_start:
                node_shape = 'doubleoctagon'  # Start node shape
            elif node.is_exit:
                node_shape = 'box'  # Exit node shape

            dot.node(node.label if node.label else str(id(node)), label_text.strip(), shape=node_shape)

        # Add edges
        for node in nodes:
            for successor, condition in node.successors:
                if condition:
                    dot.edge(node.label if node.label else str(id(node)),
                             successor.label if successor.label else str(id(successor)),
                             label=condition)  # Add condition as edge label
                else:
                    dot.edge(node.label if node.label else str(id(node)),
                             successor.label if successor.label else str(id(successor)))
        return dot

    def save_svg(self, nodes, filepath='cfg_output'):
        """Save the CFG as an SVG file."""
        graph = self.to_graphviz(nodes)
        graph.render(filepath, cleanup=True)
        print(f"CFG saved as {filepath}")

    def __repr__(self):
        return f"ControlFlowGraph with {len(self.nodes)} nodes"

