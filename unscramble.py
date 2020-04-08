#!/usr/bin/env python3
from sys import argv
import json
import random
import time

from PIL import Image
import numpy as np
from numpy import linalg


class Node(object):
    def __init__(self):
        self.img = None
        self.u = None
        self.d = None
        self.l = None
        self.r = None

    def get_edge(self, side):
        slack=1
        if side == 'u':
            return self.img.crop((0, 0, self.img.width ,slack))
        elif side == 'd':
            return self.img.crop((0, self.img.height-slack, self.img.width, self.img.height))
        elif side == 'l':
            return self.img.crop((0, 0, slack, self.img.height))
        elif side == 'r':
            return self.img.crop((self.img.width-slack, 0, self.img.width, self.img.height))


class ImGrid(object):
    def __init__(self, dims):
        self.x_dim, self.y_dim = dims
        self.xmax = self.x_dim - 1
        self.ymax = self.y_dim - 1
        self.nodes = [Node() for _ in range(self.x_dim * self.y_dim)]
        with open('nodes.json', 'r') as f:
            cons = json.loads(f.read())

        for i, vals in enumerate(cons):
            node = self.nodes[i]
            u, d, l, r = vals
            if u is not None: node.u = self.nodes[u]
            if d is not None: node.d = self.nodes[d]
            if l is not None: node.l = self.nodes[l]
            if r is not None: node.r = self.nodes[r]

    def pack(self, slices):
        for i, img in enumerate(slices):
            self.nodes[i].img = img

    @staticmethod
    def get_slices(path):
        im = Image.open(path)
        slices = []
        I = 128
        J = 128
        for j in range(0, 1920, J):
            for i in range(0, 1408, I):
                box = (i, j, i+I, j+J)
                # box = (j, i, j+J, i+I)
                slices.append(im.crop(box))

        return slices

def unscramble(img):
    pass

def test():
    seq = []

    grid = ImGrid((11, 15))
    slices = grid.get_slices('0.png')
    grid.pack(slices)
    # grid.nodes[42].img.show()
    # grid.nodes[125].img.show()
    seq.append(grid.nodes[42])
    for i in range(42, 47):

        V = np.array(grid.nodes[i].get_edge('r').getdata())
        canidates = {i:np.array(grid.nodes[i].get_edge('l').getdata()) for i in range(len(grid.nodes)) if grid.nodes[i].l is not None}
        diffs = {i:linalg.norm(V - canidates[i]) for i in canidates.keys()}

        ilow = random.choice(list(diffs.keys()))
        for i, val in diffs.items():
            if val < diffs[ilow]:
                ilow = i
        print(ilow, diffs[ilow])
        seq.append(grid.nodes[ilow])

    for node in seq:
        node.img.show()
        time.sleep(1)



if __name__ == "__main__":
    test()