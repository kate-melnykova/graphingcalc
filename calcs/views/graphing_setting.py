from decimal import Decimal
import os
import math

from matplotlib import pyplot as plt
import numpy as np
from numpy.random import randn

from views.exceptions import *
from views.convert_to_rpn import rpn
from views.implement_rpn import compute_rpn


def create_plot(raw_data):
    axes_data = raw_data['axesData']
    lines = raw_data['lines']
    print(f'Axes data is {axes_data}')
    print(f'lines are {lines}')
    figsize = [6, 6]
    try:
        figsize[0] = float(axes_data.get('figsize_x', 6))
    except (TypeError, ValueError, OverflowError):
        pass

    try:
        figsize[1] = float(axes_data.get('figsize_y', 6))
    except (TypeError, ValueError, OverflowError):
        pass

    warnings = list()
    fig, ax = plt.subplots(figsize=tuple(figsize))
    for line in lines:
        lines = SettingLine(fig, ax, line)
        warnings += lines.warnings

    axes = SettingAxes(fig, ax, axes_data)
    warnings += axes.warnings

    #filename = os.getcwd() + filepath + 'plot' + '.png'
    #plt.savefig(filename)
    #return filename
    return fig


class SettingAxes:
    # TODO: xscale, yscale
    default = {
        'title': 'y=f(x)',
        'xlabel': 'Variable x',
        'ylabel': None
    }

    def __init__(self, fig, ax, raw_data, settings={}):
        self.fig = fig
        self.ax = ax
        self.default.update(settings)
        self.raw_data = raw_data
        self.warnings = list()
        self.plot_xlabel()
        self.plot_ylabel()
        self.plot_title()
        self.plot_grid()
        self.fig.tight_layout()
        self.fig.subplots_adjust(top=0.88)

    def plot_xlabel(self):
        if self.raw_data.get('xlabel', None) is not None:
            self.ax.set_xlabel(self.raw_data['xlabel'])

    def plot_ylabel(self):
        if self.raw_data.get('ylabel', None) is not None:
            self.ax.set_ylabel(self.raw_data['ylabel'])

    def plot_title(self):
        if self.raw_data.get('title', None) is not None:
            self.fig.suptitle(self.raw_data['title'])

    def plot_grid(self):
        if self.raw_data.get('isgrid'):
            self.ax.grid()

    def plot_legend(self):
        if self.raw_data.get('legend'):
            self.ax.legend()


class SettingLine:
    default = {
        'color': 'b',
        'linewidth': 2.0,
        'linestyle': 'solid',  # 'dashed'
        'marker': None,
        'markersize': 10,
        'transparency': 1,
        'label': 'variable 1',
        'n_points': 1000,
    }

    def __init__(self, fig, ax, raw_data, settings={}):
        self.fig = fig
        self.ax = ax
        self.raw_data = raw_data
        self.default.update(settings)
        self.warnings = list()
        x_vals, y_vals = self.get_coords()
        linewidth = self.get_linewidth()
        linestyle = self.get_linestyle()
        linecolor = self.get_linecolor()
        if self.raw_data.get(f'scatterplot'):
            self.ax.scatter(x_vals, y_vals,
                            color=linecolor)
        else:
            self.ax.plot(x_vals, y_vals,
                         linewidth=linewidth,
                         linestyle=linestyle,
                         color=linecolor)

    def get_linewidth(self):
        try:
            linewidth = float(self.raw_data.get(f'linewidth', None))
        except (TypeError, ValueError, OverflowError):
            linewidth = self.default[f'linewidth']

        if linewidth <= 0:
            self.warnings.append(f'The linewidth is not positive: {linewidth}. Resetting to the default value {self.default["linewidth"]}')
            linewidth = 2.0
        return linewidth

    def get_linestyle(self):
        style = self.raw_data[f'linestyle']
        if style not in ['-', '--', '-.', '.']:
            self.warnings.append(f'Linestyle: incorrect entry: {style}')
            return self.default['style']

        else:
            return style

    def get_linecolor(self):
        return self.raw_data.get(f'linecolor', 'blue')

    def get_n_points(self):
        return self.raw_data.get('n_points{i}', self.default['n_points'])

    def get_coords(self):
        s = self.raw_data[f'expression']
        if not s:
            raise

        # covert the function to the array of values
        x_min = float(self.raw_data[f'xmin'])
        x_max = float(self.raw_data[f'xmax'])
        n_points = int(self.raw_data.get(f'n_points', self.default['n_points']))
        s = rpn(s, function=True)

        func = lambda var: compute_rpn([elem if elem != 'x' else Decimal(var) for elem in s])
        x_vals = np.linspace(x_min, x_max, n_points)
        y_vals = [func(val) for val in x_vals]

        noise = float(self.raw_data.get(f'noise', 0))
        if noise:
            std = Decimal(math.sqrt((max(y_vals) - min(y_vals)) * Decimal(noise) / 100))
            nnoise = [Decimal(x) for x in randn(len(y_vals))]
            y_vals = [y + std * n for y, n in zip(y_vals, nnoise)]
        return x_vals, y_vals


default_plot_parameters = {
                           'marker': None,
                           'markersize': 10,
                           'transparency': 1,

                           'isgrid': False,
                           'filename': 'plot.png'
                           }
