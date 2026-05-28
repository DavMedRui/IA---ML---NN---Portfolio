from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter

raiz = Node("Raíz")
hijo1 = Node("Hijo 1", parent = raiz)
hijo2 = Node("Hijo 2", parent = raiz)
hijo3 = Node("Hijo 3", parent = raiz)
nieto1 = Node("Nieto 1", parent = hijo1)
nieto2 = Node("Nieto 2", parent = hijo2)
nieto3 = Node("Nieto 3", parent = hijo3)
nieto4 = Node("Nieto 4", parent = hijo3)
bisnieto1 = Node("Bisnieto1", parent = nieto4)

print(RenderTree(raiz))
UniqueDotExporter(raiz).to_picture("raiz.png")