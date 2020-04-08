#!/usr/bin/env python3
from sys import argv
import json

from PIL import Image


class Node(object):
    def __init__(self):
        self.img = None
        self.up = None
        self.down = None
        self.left = None
        self.right = None

class ImGrid(object):
    def __init__(self, dims):
        self.x_dim, self.y_dim = dims
        self.xmax = self.x_dim - 1
        self.ymax = self.y_dim - 1
        self.nodes = [Node() for _ in range(self.x_dim * self.y_dim)]
        # self.nodes = []
        # for _ in range(self.x_dim * self.y_dim):
        #     self.nodes.append(Node())
        with open('nodes.json', 'r') as f:
            cons = json.loads(f.read())

        for i, vals in enumerate(cons):
            node = self.nodes[i]
            u, d, l, r = vals
            if u is not None: node.up = self.nodes[u]
            if d is not None: node.down = self.nodes[d]
            if l is not None: node.left = self.nodes[l]
            if r is not None: node.right = self.nodes[r]

    def pack(self, slices):
        for i, img in enumerate(slices):
            self.nodes[i].img = img


def unscramble(img):
    pass


def test():
    im = Image.open('1.png')
    slices = []
    I = 128
    J = 128
    for j in range(0, 1920, J):
        for i in range(0, 1408, I):
            print(i, j)
            box = (i, j, i+I, j+J)
            # box = (j, i, j+J, i+I)
            slices.append(im.crop(box))

    grid = ImGrid((11, 15))
    grid.pack(slices)
    grid.nodes[30].img.show()
    grid.nodes[30].up.img.show()
    grid.nodes[30].left.img.show()



if __name__ == "__main__":
    test()