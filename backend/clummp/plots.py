from astropy.io import fits
import matplotlib 
import matplotlib.pyplot as plt, mpld3
import numpy as np 


def side_by_side_plot(path1, path2):
    data1 = fits.getdata(path1)
    data2 = fits.getdata(path2)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(data1, aspect='equal')
    ax2.imshow(data2, aspect='equal')
    ax1.tick_params(bottom=False, top=False, left=False, right=False)
    ax2.tick_params(bottom=False, top=False, left=False, right=False)
    return mpld3.fig_to_html(fig)

