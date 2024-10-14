import re
from riscvflow.utils import get_zeros


class CFGNode:
    """Represents a node in the control flow graph."""

    def __init__(self, label=None):
        self.label = label  # Function or block label
        self.ast_nodes = []  # Abstract Syntax Tree nodes (instructions or labels)
        self.successors = []  # Successors in the control flow
        self.is_exit = False  # To mark this node as an exit node
        self.is_start = False  # To mark this node as the start node
        self.is_macro = False  # To mark this node as a macro
        self.is_function_start = False  # To mark this node as a function
        self.is_function_exit = False  # To mark this node as a function exit

    def add_successor(self, node, condition):
        self.successors.append((node, condition))

    def add_ast_node(self, ast_node):
        """Add an AST node (instruction or label) to this block."""
        self.ast_nodes.append(ast_node)

    def __repr__(self):
        return f"CFGNode({self.label})"

    @property
    def children(self):
        """Return the children nodes of this block."""
        return [succ for succ, _ in self.successors]


class LabelNode:
    """Represents a label in the instruction set."""

    def __init__(self, line_no, label):
        self.line_no = line_no
        self.label = label

    def __repr__(self):
        return f"#{get_zeros(self.line_no)}: {self.label}"


class InstructionNode:
    """Represents an instruction in the control flow graph."""

    def __init__(self, line_no, instruction):
        self.line_no = line_no
        self.instruction = instruction
        # Extract the comment if it exists
        comment_match = re.search(r'#.*', instruction)
        if comment_match:
            self.comment = comment_match.group(0).strip()
            self.code = instruction[:comment_match.start()].strip()  # Code without comment
        else:
            self.comment = None
            self.code = instruction

    def __repr__(self):
        # Set a fixed width for the instruction part to align the comments
        padding = 40  # You can adjust the padding to fit your needs
        padded_code = f"#{get_zeros(self.line_no)}: {self.code:<{padding}}"  # Left-align and pad the instruction
        if self.comment:
            return f"{padded_code} {self.comment}"
        return f"{padded_code}"

    @property
    def command(self):
        return self.code.split()[0]


class MacroNode:
    """Represents a macro in the control flow graph."""

    def __init__(self, start_line, label):
        self.ast_nodes = []
        self.line_start = start_line
        self.label = label
        self.line_end = None
        self.successors = []
        self.is_macro = True
        self.is_exit = False
        self.is_start = False

    def add_ast_node(self, ast_node):
        """Add an AST node (instruction or label) to this block."""
        self.ast_nodes.append(ast_node)

    def set_end_line(self, end_line):
        self.line_end = end_line

    def __repr__(self):
        return f"MacroNode({self.line_start}, {self.line_end})"


class FunctionNode:
    """Represents a function in the control flow graph."""

    def __init__(self, label):
        self.label = label  # The function name (label)
        self.nodes = []  # List of basic blocks in the function
        self.entry_node = None  # Entry node (first block)
        self.exit_node = None  # Exit node (block with jalr)

    def add_node(self, node):
        self.nodes.append(node)

    def set_entry_node(self, node):
        self.entry_node = node

    def set_exit_node(self, node):
        self.exit_node = node

    def __repr__(self):
        return f"FunctionNode(label={self.label}, entry={self.entry_node}, exit={self.exit_node})"

