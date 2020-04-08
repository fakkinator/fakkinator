#!/usr/bin/env python3
from sys import argv
import json

from PIL import Image


class Node(object):
    def __init__(self):
        self.img = None
        self.u = None
        self.d = None
        self.l = None
        self.r = None

    def get_edge(self, side):
        if side == 'u':
            return self.img.crop((0, 0, self.img.width ,1))
        elif side == 'd':
            return self.img.crop((0, self.img.height-1, self.img.width, self.img.height))
        elif side == 'l':
            return self.img.crop((0, 0, 1, self.img.height))
        elif side == 'r':
            return self.img.crop((self.img.width-1, 0, self.img.width, self.img.height))


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
                print(i, j)
                box = (i, j, i+I, j+J)
                # box = (j, i, j+J, i+I)
                slices.append(im.crop(box))

        return slices

def unscramble(img):
    pass

def test():

    grid = ImGrid((11, 15))
    slices = grid.get_slices('1.png')
    grid.pack(slices)



if __name__ == "__main__":
    test()