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

    def __getitem__(self, key):
        if key == 'u':
            return self.u
        elif key == 'd':
            return self.d
        elif key == 'l':
            return self.l
        elif key == 'r':
            return self.r
        else:
            return None

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

    def dist(self, node, side_a, side_b):
        side_a_img = self.get_edge(side_a)
        side_a_arr = np.array(side_a_img.getdata())
        side_b_img = node.get_edge(side_b)
        side_b_arr = np.array(side_b_img.getdata())

        return linalg.norm(side_a_arr - side_b_arr)

    def get_surround_dist(self):
        tot = 0
        if self.u:
            tot += self.dist(self.u, 'u', 'd')
        if self.d:
            tot += self.dist(self.d, 'd', 'u')
        if self.l:
            tot += self.dist(self.l, 'l', 'r')
        if self.r:
            tot += self.dist(self.r, 'r', 'l')
        return tot


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

    def get_canidates(self, side):
        canidates = {}
        for i, node in enumerate(self.nodes):
            if node[side] is not None:
                canidates[i] = node[side]
        return canidates
            
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

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def test2():
    grid = ImGrid((11, 15))
    slices = grid.get_slices('0.png')
    grid.pack(slices)
    used = []
    for i in range(70, 75):
        nodei = grid.nodes[i]
        dists = [nodei.dist(node, 'r', 'l') for node in grid.nodes]
        print(dists)
        imin = np.argmin(dists)
        print(imin)
        nodeimin = grid.nodes[imin]
        while nodeimin in used:
            dists.pop(imin)
            imin = np.argmin(dists)
            nodeimin = grid.nodes[imin]
        t = grid.nodes[i+1].img
        grid.nodes[i+1].img = nodeimin.img
        nodeimin.img = t
        used.append(grid.nodes[i+1])
        used.append(nodeimin)

    for i in range(25, 30):
        grid.nodes[i].img.show()
        time.sleep(1)

    print()


    # construct strips
    # for y in range(15):
    #     for x in range(10):
    #         V = np.array(grid.nodes[pos].get_edge('l').getdata())
    #         canidates = {
    #             i:np.array(grid.nodes[i].get_edge('r').getdata()) for i in range(len(grid.nodes)) if grid.nodes[i].l is not None
    #         }
    #         diffs = {i:linalg.norm(V - canidates[i]) for i in canidates.keys()}

    #         ilow = random.choice(list(diffs.keys()))
    #         for j, val in diffs.items():
    #             if val < diffs[ilow]:
    #                 ilow = j

    #         t = grid.nodes[ilow].img
    #         grid.nodes[ilow].img = grid.nodes[pos+1].img
    #         grid.nodes[pos+1].img = t

    #         pos += 1

    # outims = []
    # os = 0
    # for os in range(15):
    #     im = grid.nodes[0+os*11].img
    #     for i in range(1, 11):
    #         im = get_concat_h(im, grid.nodes[i+os].img)
    #     outims.append(im)

    # outim = outims[0]
    # for i in range(1, 15):
    #     outim = get_concat_v(outim, outims[i])
    # imout = grid.nodes[30].img
    # w, l = 1408, 1920
    # imout = Image.new('RGB', (w, l))
    # pos = 0
    # for j in range(1, l, 128):
    #     for i in range(1, w, 128):
    #         imout.paste(grid.nodes[pos].img, (i, j))
    #         pos += 1
    
    # imout.show()


def test():

    grid = ImGrid((11, 15))
    slices = grid.get_slices('0.png')
    grid.pack(slices)
    # grid.nodes[42].img.show()
    # grid.nodes[125].img.show()
    i = 0
    seq = [grid.nodes[i]]
    for _ in range(0, 10):
        nodei = grid.nodes[i]
        if nodei.u is not None:
            pass

        if nodei.l is not None:
            pass

        V = np.array(grid.nodes[i].get_edge('l').getdata())
        canidates = {
            i:np.array(grid.nodes[i].get_edge('r').getdata()) for i in range(len(grid.nodes)) if grid.nodes[i].l is not None
        }
        diffs = {i:linalg.norm(V - canidates[i]) for i in canidates.keys()}

        ilow = random.choice(list(diffs.keys()))
        for i, val in diffs.items():
            if val < diffs[ilow]:
                ilow = i
        print(ilow, diffs[ilow])
        i = ilow
        seq.append(grid.nodes[ilow])

    for node in seq:
        node.img.show()
        time.sleep(1)



if __name__ == "__main__":
    test2()