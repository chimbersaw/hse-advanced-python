import ast

import networkx as nx

nodes_to_vertices = {
    ast.FunctionDef: (lambda x: f"Function: {x.name}", "#cfb53b"),
    ast.arg: (lambda x: f"Argument: {x.arg}", "#f78fa7"),
    ast.Name: (lambda x: f"Name: {x.id}", "#addfad"),
    ast.Constant: (lambda x: f"Constant: {x.value}", "#b44c43"),
    ast.Sub: (lambda _: "-", "#ddbec3"),
    ast.Module: (None, "#543964"),
    ast.arguments: (None, "#6c6960"),
    ast.If: (None, "#826c34"),
    ast.Return: (None, "#fddb6d"),
    ast.Compare: (None, "#00ff00"),
    ast.BinOp: (None, "#ff5349"),
    ast.Call: (None, "#8f509d"),
    ast.Add: (None, "#1fcecb"),
    ast.ListComp: (None, "#a6caf0"),
    ast.comprehension: (None, "#ff00ff"),
    ast.Store: (None, "#7fffd4"),
    ast.LtE: (None, "#a5694f"),
    ast.Load: (lambda _: None, None)
}


def get_color_and_label(node):
    clz = node.__class__
    default = None, "#ffffff"
    node_to_label, color = nodes_to_vertices.get(clz, default)

    if node_to_label is not None:
        label = node_to_label(node)
    else:
        label = clz.__name__
    return label, color


class Graph:
    def __init__(self, graph=nx.DiGraph()):
        self.graph = graph

    def visit(self, node):
        label, color = get_color_and_label(node)
        if label is None:
            return False
        self.graph.add_node(node, label=label, color=color, shape="rect", style="filled")
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        if self.visit(item):
                            self.graph.add_edge(node, item)
            elif isinstance(value, ast.AST):
                if self.visit(value):
                    self.graph.add_edge(node, value)
        return True


def main():
    with open("fib.py") as file:
        code = file.read()
    tree = ast.parse(code)
    g = Graph()
    g.visit(tree)
    nx.drawing.nx_pydot.to_pydot(g.graph).write_png("artifacts/fib.png")


if __name__ == "__main__":
    main()
