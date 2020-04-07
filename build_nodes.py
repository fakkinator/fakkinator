from sys import argv

def build_nodes(xdim, ydim):
    print('[')
    i = 0
    for y in range(ydim):
        for x in range(xdim):
            print("[{},{},{},{}],".format(
                i-xdim if y is not 0 else 'null',
                i+xdim if y is not ydim-1 else 'null',
                i-1 if x is not 0 else 'null',
                i+1 if x is not xdim-1 else 'null',
            ))
            i += 1
    print(']')

if __name__ == "__main__":
    _, xdim, ydim = argv
    xdim = int(xdim)
    ydim = int(ydim)
    build_nodes(xdim, ydim)