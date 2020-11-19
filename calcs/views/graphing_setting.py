from decimal import Decimal

from matplotlib import pyplot as plt
import numpy as np

from views.exceptions import *
from views.convert_to_rpn import rpn
from views.implement_rpn import compute_rpn


class SettingAxes:
    # TODO: xscale, yscale
    default = {
        'title': 'y=f(x)',
        'xlabel': 'Variable x',
        'ylabel': None
    }

    def __init__(self, fig, ax, row_data, settings={}):
        self.fig = fig
        self.ax = ax
        self.default.update(settings)
        self.row_data = row_data
        self.warnings = list()
        self.plot_xlabel()
        self.plot_ylabel()
        self.plot_title()

    def plot_xlabel(self):
        if self.raw_data.get('xlabel', None) is not None:
            self.ax.set_xlabel(self.raw_data['xlabel'])

    def plot_ylabel(self):
        if self.raw_data.get('ylabel', None) is not None:
            self.ax.set_ylabel(self.raw_data['ylabel'])

    def plot_title(self, fig):
        if self.raw_data.get('title', None) is None:
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
        x_vals, y_vals = self.get_coords()
        linewidth = self.get_linewidth()
        style = self.get_linewidth()
        self.ax.plot(x_vals, y_vals, linewidth=linewidth, style=style)

    def get_linewidth(self):
        try:
            linewidth = float(self.raw_data.get('linewidth', None))
        except (TypeError, ValueError, OverflowError):
            linewidth = self.default['linewidth']

        if linewidth <= 0:
            self.warnings.append(f'The linewidth is not positive: {linewidth}. Resetting to the default value {self.default["linewidth"]}')
            linewidth = 2.0
        return linewidth

    def get_linestyle(self):
        style = self.raw_data['linestyle']
        if style not in ['-', '--', '-.', '.']:
            self.warnings.append(f'Linestyle: incorrect entry: {style}')
            return self.default['style']

        else:
            return style

    def get_coords(self):
        # covert the function to the array of values
        x_min = float(self.raw_data['xmin'])
        x_max = float(self.raw_data['xmax'])
        s = self.raw_data['expression']
        n_points = int(self.raw_data.get('n_points', self.default['n_points']))
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
