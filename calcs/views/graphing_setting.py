from decimal import Decimal
import os

from matplotlib import pyplot as plt
import numpy as np
from uuid import uuid4

from views.exceptions import *
from views.convert_to_rpn import rpn
from views.implement_rpn import compute_rpn


def create_plot(raw_data, filepath):
    figsize = [6, 6]
    try:
        figsize[0] = float(raw_data.get('figsize_x', 6))
    except (TypeError, ValueError, OverflowError):
        pass

    try:
        figsize[1] = float(raw_data.get('figsize_y', 6))
    except (TypeError, ValueError, OverflowError):
        pass

    warnings = list()
    fig, ax = plt.subplots(figsize=tuple(figsize))
    axes = SettingAxes(fig, ax, raw_data)
    warnings += axes.warnings

    lines = SettingLine(fig, ax, raw_data)
    warnings += lines.warnings

    filename = os.getcwd() + filepath + 'plot' + '.png'
    plt.savefig(filename)
    return filename


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
        for i in range(1, 4):
            try:
                x_vals, y_vals = self.get_coords(i)
            except:
                break
            linewidth = self.get_linewidth(i)
            linestyle = self.get_linestyle(i)
            linecolor = self.get_linecolor(i)
            if self.raw_data.get(f'scatterplot{i}'):
                self.ax.scatter(x_vals, y_vals,
                                color=linecolor)
            else:
                self.ax.plot(x_vals, y_vals,
                             linewidth=linewidth,
                             linestyle=linestyle,
                             color=linecolor)

    def get_linewidth(self, i: int):
        try:
            linewidth = float(self.raw_data.get(f'linewidth{i}', None))
        except (TypeError, ValueError, OverflowError):
            linewidth = self.default[f'linewidth{i}']

        if linewidth <= 0:
            self.warnings.append(f'The linewidth is not positive: {linewidth}. Resetting to the default value {self.default["linewidth"]}')
            linewidth = 2.0
        return linewidth

    def get_linestyle(self, i: int):
        style = self.raw_data[f'linestyle{i}']
        if style not in ['-', '--', '-.', '.']:
            self.warnings.append(f'Linestyle: incorrect entry: {style}')
            return self.default['style']

        else:
            return style

    def get_linecolor(self, i: int):
        return self.raw_data.get(f'linecolor{i}', 'blue')

    def get_n_points(self, i: int):
        return self.raw_data.get('n_points{i}', self.default['n_points'])

    def get_coords(self, i: int):
        s = self.raw_data[f'expression{i}']
        if not s:
            raise

        # covert the function to the array of values
        x_min = float(self.raw_data[f'xmin{i}'])
        x_max = float(self.raw_data[f'xmax{i}'])
        n_points = int(self.raw_data.get(f'n_points{i}', self.default['n_points']))
        assert x_min < x_max  # TODO: add to validators
        s = rpn(s, function=True)

        func = lambda var: compute_rpn([elem if elem != 'x' else Decimal(var) for elem in s])
        x_vals = np.linspace(x_min, x_max, n_points)
        y_vals = [func(val) for val in x_vals]
        return x_vals, y_vals


default_plot_parameters = {
                           'marker': None,
                           'markersize': 10,
                           'transparency': 1,

                           'isgrid': False,
                           'filename': 'plot.png'
                           }
