#!/usr/bin/python3
import sys
import numpy as np
from painter_play import painter_play
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print('Run: python3 %s rule_filename room_filename\n'
              'filenames are expected to be .npy.' % (sys.argv[0]))
        sys.exit(1)

    rule = np.load(sys.argv[1])  # load rule
    room = np.load(sys.argv[2])  # load room

    s, x_pos, y_pos, env = painter_play(rule, room)
    print("Room shape:", room.shape, ",score:", s)
    x = np.array(x_pos) + 0.5
    y = np.array(y_pos) + 0.5
    cmap = ListedColormap(["whitesmoke", "darkslategrey", "powderblue"])
    data = env
    fig, ax = plt.subplots()
    psm = ax.pcolormesh(data, cmap=cmap, rasterized=True)
    ax.plot(y, x, 'k-')
    ax.plot(y[0], x[0], 'r.', markersize=10)
    ax.plot(y[-1], x[-1], 'k.', markersize=10)
    plt.axis('scaled')
    plt.show()
