import TreeRegression as tr
import math
import matplotlib.pyplot as plt
import numpy as np


points = [tr.Point(i, math.sin(i / 15)) for i in range(30)]
# points = [tr.Point(i, i * i) for i in range(20)]

rss = []


def plots(left: list[tr.Point], right: list[tr.Point], ds):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    lx, ly = tr.Tree.separate_xy(left)
    ax1.scatter(lx, ly)
    rx, ry = tr.Tree.separate_xy(right)
    lax = np.average(lx)
    lay = np.average(ly)
    ax1.scatter(lax, lay)
    rax = np.average(rx)
    ray = np.average(ry)
    ax1.scatter(rx, ry)
    ax1.scatter(rax, ray)
    ax2.scatter([range(len(ds))], ds)
    plt.show()


def plots2(points: list[tr.Point], nodes: list[tr.Node]):
    x = [p.x for p in points]
    y = [p.y for p in points]
    plt.scatter(x, y)
    predicts = [tree_pass(nodes, f.x) for f in points]
    plt.scatter([range(len(points))], predicts)
    plt.show()


node = tr.Tree(points, 0, "Base")

#  for i in range(30):
# for p in points:
#     print(p.get())


def find_next_node(node: tr.Node, side_: str) -> tr.Node:
    for n in tr.Tree.nodes:
        if n.parent == node.id and n.side == side_:
            return n
    return tr.Tree.nodes[0]


def tree_pass(nodes: list[tr.Node], x_: float):
    side = ""
    prediction = 0

    node: tr.Node = nodes[0]
    while True:
        print(node)
        prediction = node.prediction
        if x_ < node.splitter:
            side = "left"
        else:
            side = "right"
        node = find_next_node(node, side)
        if node == nodes[0]:
            break
    print("="*100)
    return prediction


print("-"*100)

# n = float(input("input checking number: "))
# print(tree_pass(nodes, n))
plots2(points, tr.Tree.nodes)
