import numpy as np
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get(self):
        return [self.x, self.y]


class Node:
    def __init__(self,
                 id: int,
                 parent: int,
                 side: str,
                 len_left: int,
                 len_right: int,
                 splitter: float,
                 prediction: float,
                 left: list[Point],
                 right: list[Point]):
        self.id = id
        self.parent = parent
        self.side = side
        self.len_left = len_left
        self.len_right = len_right
        self.splitter = splitter
        self.prediction = prediction
        self.left = left
        self.right = right

    def __str__(self):
        return f'Node {self.id}: ' \
               f'parent={self.parent}, ' \
               f'side={self.side}, ' \
               f'len_left={self.len_left}, ' \
               f'len_right={self.len_right}, ' \
               f'splitter={self.splitter}, ' \
               f'prediction={self.prediction}, ' \
               f'left={[p.x for p in self.left]}, ' \
               f'right={[p.x for p in self.right]}'



class Tree:
    tag = 0
    min_points = 10
    nodes: list[Node] = []

    def __init__(self, points_: list[Point], parent_node, side: str):
        self.side = side
        self.id = Tree.tag
        Tree.tag += 1
        self.parent_node = parent_node
        self.points = points_
        self.prediction = self.y_average(self.points)
        print([p.get() for p in points_], self.prediction)
        if len(self.points) < Tree.min_points:
            node: Node = Node(self.id,
                              parent_node,
                              side,
                              0,
                              0,
                              0,
                              self.prediction,
                              [],
                              [])
            Tree.nodes.append(node)
            print(f'Leaf: {node}')
            return
        best_left, best_right, best_p = self.search_best_split(self.points)
        # self.plot_best_split(best_left, best_right, best_p)
        node: Node = Node(self.id,
                          parent_node,
                          side,
                          len(best_left),
                          len(best_right),
                          best_p.x,
                          self.prediction,
                          best_left,
                          best_right)
        print(node)
        Tree.nodes.append(node)
        self.left = Tree(best_left, self.id, "left")
        self.right = Tree(best_right, self.id, "right")
        self.p = best_p

    def plot_best_split(self, best_left, best_right, best_p):
        xl, yl = self.separate_xy(best_left)
        xr, yr = self.separate_xy(best_right)
        plt.scatter(xl, yl)
        plt.scatter(xr, yr)
        plt.scatter(best_p.x, best_p.y)
        plt.show()

    def y_average(self, points_):
        return np.average([p.y for p in points_])

    def RSS(self, points_):
        xs, ys = self.separate_xy(points_)
        a = np.average(ys)
        d = 0
        for y in ys:
            d = (y - a) ** 2
        return d

    def split(self, points_: list[Point], t: Point) -> {list[Point], list[Point]}:
        left = []
        right = []
        for p in points_:
            if p.x < t.x:
                left.append(p)
            else:
                right.append(p)
        return left, right

    def search_best_split(self, points_: list[Point]) -> {list[Point], list[Point]}:
        best_rss = 10e8
        best_left: list[Point] = []
        best_right: list[Point] = []
        ds: list[float] = []
        best_p: Point = points_[0]
        for p in points_:
            left, right = self.split(points_, p)
            if len(left) == 0 or len(right) == 0:
                continue
            rss_left = self.RSS(left)
            rss_right = self.RSS(right)
            rss = rss_left + rss_right
            ds.append(rss)
            if rss < best_rss:
                best_rss = rss
                best_left = left
                best_right = right
                best_p = p
        for p in points_:
            print(p.get())
        print(ds)
        print("+" * 100)
        return best_left, best_right, best_p

    def separate_xy(self, points_):
        x = [p.x for p in points_]
        y = [p.y for p in points_]
        return x, y
