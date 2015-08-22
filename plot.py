
"""
When plotting daily data, a frequent request is to plot the data
ignoring skips, eg no extra spaces for weekends.  This is particularly
common in financial time series, when you may have data for M-F and
not Sat, Sun and you don't want gaps in the x axis.  The approach is
to simply use the integer index for the xdata and a custom tick
Formatter to get the appropriate date string for a given index.
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import Formatter
import matplotlib.rcsetup
import matplotlib

class MyFormatter(Formatter):

    def __init__(self, dates, fmt='%Y-%m-%d'):
        self.dates = dates
        self.fmt = fmt

    def __call__(self, x, pos=0):
        'Return the label for time x at position pos'
        ind = int(round(x))
        if ind >= len(self.dates) or ind < 0:
            return ''

        return self.dates[ind].strftime(self.fmt)


def plot(dates, linelist, backend=None):
    formatter = MyFormatter(dates)

    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(formatter)
    for data, colorcode in linelist:
        ax.plot(range(len(data)), data, colorcode)
    fig.autofmt_xdate()

    for backend in matplotlib.rcsetup.all_backends:
        matplotlib.rcParams['backend'] = backend
        print 'trying to show with %s' % backend
        print 'plt.show(%s) = %s' % (backend, plt.show())
