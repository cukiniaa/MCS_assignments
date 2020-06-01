#!/usr/bin/python3
import sys
import numpy as np
import matplotlib.pyplot as plt
# plt.rcParams.update({'font.size': 20})


def format_coord(x, y):
    col = int(x + 0.5)
    row = int(y + 0.5)
    if col >= 0 and col < numcols and row >= 0 and row < numrows:
        z = X[row, col]
        return 'x=%1.4f, y=%1.4f, z=%1.4f' % (x, y, z)
    else:
        return 'x=%1.4f, y=%1.4f' % (x, y)


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print('Run: python3 %s filename\nfilename is expected to be '
              '.npy, (ex. generation.npy).' % (sys.argv[0]))
        sys.exit(1)

    generation = np.load(sys.argv[1])  # load generation
    X = generation.T

    fig, ax = plt.subplots()
    ax.imshow(X, interpolation='nearest')
    numrows, numcols = X.shape
    print("Generation with %d individuals." % numcols)
    # print("0 - purple, 1 - blue, 2 - green, 3 - yellow")
    ax.format_coord = format_coord
    plt.xlabel("Generation")
    plt.ylabel("Centers of clusters")
    plt.show()
