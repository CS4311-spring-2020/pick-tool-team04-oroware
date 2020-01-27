#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import matplotlib.pyplot as plt

plt.ion()

fig, ax = plt.subplots()

def on_key_press(event):
    if event.key == 'enter':
        ans = input('Provide some text to print and press enter:\n')
        # ans = 'foo'
        ax.text(event.xdata, event.ydata, ans)
        fig.canvas.draw_idle()

cid = fig.canvas.mpl_connect('key_press_event', on_key_press)
