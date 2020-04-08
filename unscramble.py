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
    def __init__(self, node_dims, img_dims):
        self.img_dims = img_dims
        self.x_dim, self.y_dim = node_dims
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
    
    def __getitem__(self, key):
        return self.nodes[key]

    def pack(self, slices):
        for i, img in enumerate(slices):
            self.nodes[i].img = img

    def flip(self, a, b):
        if isinstance(a, Node):
            node_a = a
        else:
            node_a = self.nodes[a]

        if isinstance(b, Node):
            node_b = b
        else:
            node_b = self.nodes[b]

        t = node_a.img
        node_a.img = node_b.img
        node_b.img = t

    def get_canidates(self, side):
        canidates = {}
        for i, node in enumerate(self.nodes):
            if node[side] is not None:
                canidates[i] = node[side]
        return canidates

    def build_img(self):
        w, l = self.img_dims
        imout = Image.new('RGB', (w, l))
        pos = 0
        for j in range(1, l, 128):
            for i in range(1, w, 128):
                imout.paste(self.nodes[pos].img, (i, j))
                pos += 1
        
        return imout

    def dump_cells(self, path):
        for i, node in enumerate(self.nodes):
            node.img.save('{}/{}.png'.format(path, i))
            
    @staticmethod
    def get_slices(path, img_dims):
        W, L = img_dims
        im = Image.open(path)
        slices = []
        I = 128
        J = 128
        for j in range(0, L, J):
            for i in range(0, W, I):
                box = (i, j, i+I, j+J)
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
    W, L = 3, 3
    img_dims = (384, 384)
    grid = ImGrid((L, W), img_dims)
    slices = grid.get_slices('0.png', img_dims)
    grid.pack(slices)

    for _ in range(1):
        for i in range(0, L*W):
            if not grid[i].r:
                continue
            dists = [grid[i].dist(node, 'r', 'l') for node in grid.nodes]
            imin = np.argmin(dists)
            print(i, imin, min(dists))
            grid.flip(grid[i].r, imin)


    # for _ in range(1):
    #     for i in range(0, 11*15):
    #         if not grid[i].r:
    #             continue
    #         dists = [grid[i].dist(node, 'r', 'l') for node in grid.nodes]
    #         imin = np.argmin(dists)
    #         print(i, imin, min(dists))
    #         t = grid[i].r.img
    #         grid[i].r.img = grid[imin].img
    #         grid[imin].img = t

    # grid.build_img().save('test3.png')
    grid.build_img().show()


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
