#!/usr/bin/python3
import sys
import numpy as np
from painter_play import painter_play
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from time import sleep

if __name__ == "__main__":
    if(len(sys.argv) < 4):
        print('Run: python3 %s rule_filename room_filename [animation]\n'
              'filenames are expected to be .npy.\n'
              'If you write true as the last parameter,\nthe trajectory  '
              'will be displayed as an animation.' % (sys.argv[0]))
        sys.exit(1)
    animation = False
    if len(sys.argv) > 3:
        animation = (sys.argv[3].lower() == 'true')

    rule = np.load(sys.argv[1])  # load rule
    room = np.load(sys.argv[2])  # load room

    s, x_pos, y_pos, env = painter_play(rule, room)
    print("Room shape:", room.shape, ",score:", s)
    x = np.array(x_pos) + 0.5
    y = np.array(y_pos) + 0.5

    if animation:
        plt.ion()

    cmap = ListedColormap(["whitesmoke", "darkslategrey", "powderblue"])
    data = env
    fig, ax = plt.subplots()
    psm = ax.pcolormesh(data, cmap=cmap, rasterized=True)
    plt.axis('scaled')

    if animation:
        ax.plot(y[0], x[0], 'r.', markersize=10)
        for i in range(1, len(x)):
            ax.plot([y[i-1], y[i]], [x[i-1], x[i]], 'k-')
            fig.canvas.draw()
            fig.canvas.flush_events()
            sleep(0.05)
        ax.plot(y[-1], x[-1], 'k.', markersize=10)
    else:
        ax.plot(y, x, 'k-')
        ax.plot(y[0], x[0], 'r.', markersize=10)
        ax.plot(y[-1], x[-1], 'k.', markersize=10)
        plt.show()
