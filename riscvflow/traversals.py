
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


def listMacros(cfg):
    macros = []
    for node in cfg.nodes:
        if node.is_macro:
            macros.append(node)
    return macros
