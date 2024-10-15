import re
from riscvflow.node import CFGNode, InstructionNode
from riscvflow.registers import all_registers


def dfsVisited(cfg, start_label):
    visited = set()
    stack = [cfg[start_label]]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        children = node.children
        succ = node.successors
        print(f"{node.label} -> {[child.label for child in children]} | {[(s[0].label, s[1]) for s in succ]}")
        for child in node.children:
            stack.append(child)
    return visited


def dfsFunction(cfg, start_label):
    visited = set()
    stack = [cfg[start_label]]
    first = True
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        if not first and (node.is_function_exit or node.is_exit or node.is_function_start):
            continue
        visited.add(node)
        first = False
        for child in node.children:
            stack.append(child)
    return visited


def getFunctions(cfg, start_label, function_list):
    visited = set()
    stack = [cfg[start_label]]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        print('Node:', node.label, node.is_function_start)
        if node.is_function_start:
            function_list.append(node.label)
        for child in node.children:
            stack.append(child)
    return visited


def nestedFunctions(cfg, start_label):
    visited = set()
    stack = [cfg[start_label]]
    first = True
    possible_functions = []
    function_regex = re.compile(r'jal\s+ra\s*,\s*(\w+)')
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        if not first and (node.is_function_exit or node.is_exit or node.is_function_start):
            continue
        visited.add(node)
        for ast_node in node.ast_nodes:
            if isinstance(ast_node, InstructionNode):
                match = function_regex.match(ast_node.code)
                if match:
                    possible_functions.append(match.group(1))
        first = False
        for child in node.children:
            stack.append

    return possible_functions


class RegisterGraph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, node, edge):
        if node not in self.graph:
            self.graph[node] = []
        self.graph[node].append(edge)

    def get_graph(self):
        return self.graph

    def __repr__(self):
        return str(self.graph)


def registerUsage(cfg, start_label):
    visited = set()
    stack = [cfg[start_label]]
    first = True
    inst_arg_2 = re.compile(r'(\w+)\s+(\w+),\s*(-?\d+\(\w+\)|\w+)')
    inst_arg_3 = re.compile(r'(\w+)\s+(\w+),\s*(-?\d+\(\w+\)|\w+),\s*(-?\d+\(\w+\)|\w+)')
    offset_reg = re.compile(r'(-?\d+)\((\w+)\)')

    reg_graph = RegisterGraph()
    regs = all_registers()

    def get_registers(instruction):
        command = instruction.count(',')
        if command == 2:
            match = inst_arg_3.match(instruction)
            if match:
                offset_reg_match_4 = offset_reg.match(match.group(4))
                offset_reg_match_3 = offset_reg.match(match.group(3))
                reg_4 = match.group(4)
                reg_3 = match.group(3)
                if offset_reg_match_4:
                    reg_4 = offset_reg_match_4.group(2)
                if offset_reg_match_3:
                    reg_3 = offset_reg_match_3.group(2)
                reg_2 = match.group(2)
                reg_list = [reg_2]
                if regs.search(reg_3):
                    reg_list.append(reg_3)
                if regs.search(reg_4):
                    reg_list.append(reg_4)
                return reg_list
        elif command == 1:
            match = inst_arg_2.match(instruction)
            if match:
                offset_reg_match = offset_reg.match(match.group(3))
                reg_3 = match.group(3)
                if offset_reg_match:
                    reg_3 = offset_reg_match.group(2)
                if regs.search(reg_3):
                    return [match.group(2), reg_3]
                return [match.group(2)]
        return []

    def add_dependencies(registers):
        """Add edges for register dependencies (sources -> destination)."""

        if len(registers) == 3:
            dest_reg = registers[0]
            source_regs = registers[1:]
            for src in source_regs:
                if offset_reg.match(src):  # Handle the case where src is like 4(sp)
                    src = offset_reg.match(src).group(2)  # Extract register from offset
                reg_graph.add_edge(src, dest_reg)
        elif len(registers) == 2:
            dest_reg = registers[0]
            src_reg = registers[1]
            if offset_reg.match(src_reg):  # Handle the case where src is like 4(sp)
                src_reg = offset_reg.match(src_reg).group(2)  # Extract register from offset
            reg_graph.add_edge(src_reg, dest_reg)

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        if not first and (node.is_function_exit or node.is_exit or node.is_function_start):
            continue
        visited.add(node)
        for ast_node in node.ast_nodes:
            instruction = ast_node.code.strip()
            registers = get_registers(instruction)
            print(instruction, registers)
            if registers:
                add_dependencies(registers)
        first = False
        for child in node.children:
            stack.append
    return reg_graph


def listMacros(cfg):
    macros = []
    for node in cfg.nodes:
        if node.is_macro:
            macros.append(node)
    return macros
