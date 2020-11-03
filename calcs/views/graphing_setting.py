from matplotlib import pyplot as plt
import numpy as np


class SettingAxes:
    # TODO: xscale, yscale
    default_axes_properties = {
        'figsize': (6, 6),

        'showtitle': False,
        'title': 'y=f(x)',

        'showxlabel': False,
        'xlabel': 'Variable x',

        'showylabel': False,
        'ylabel': None
    }

    @classmethod
    def make_params(cls, raw_data):
        params = dict(cls.default_axes_properties)
        warnings = list()

        params['figsize'] = cls.process_figsize(raw_data, warnings)
        params['showxlabel'], params['xlabel'] = cls.process_xlabel(raw_data, warnings)
        params['showylabel'], params['ylabel'] = cls.process_ylabel(raw_data, warnings)
        params['showtitle'], params['title'] = cls.process_title(raw_data, warnings)
        return params, warnings

    @classmethod
    def process_figsize(cls, raw_data, warnings=[]):
        # figsize
        figsize_x = raw_data.get('figsize_x', cls.default_axes_properties['figsize'][0])
        figsize_y = raw_data.get('figsize_y', cls.default_axes_properties['figsize'][1])
        figsize = cls.default_axes_properties['figsize']
        figsize = list(figsize)
        try:
            figsize_x = float(figsize_x)
        except (ValueError, OverflowError):
            warnings.append(f'Incorrect width of the figure: {figsize_x}')
        else:
            figsize[0] = figsize_x

        try:
            figsize_y = float(figsize_y)
        except (TypeError, ValueError, OverflowError):
            warnings.append(f'Incorrect width of the figure: {figsize_y}')
        else:
            figsize[1] = figsize_y

        return tuple(figsize)

    @classmethod
    def process_xlabel(cls, raw_data, warnings=[]):
        if raw_data.get('xlabel', None) is None:
            return False, None

        return True, raw_data['xlabel']

    @classmethod
    def process_ylabel(cls, raw_data, warnings=[]):
        if raw_data.get('ylabel', None) is None:
            return False, None

        return True, raw_data['ylabel']

    @classmethod
    def process_title(cls, raw_data, warnings=[]):
        if raw_data.get('title', None) is None:
            return False, None

        return True, raw_data['title']

    @classmethod
    def make_plot(cls, raw_data):
        params, warnings = cls.make_params(raw_data)
        fig = plt.figure(figsize=params['figsize'])
        if params['showtitle']:
            fig.suptitle(params['title'])
        if params['showxlabel']:
            plt.xlabel(params['xlabel'])
        if params['showylabel']:
            plt.ylabel(params['ylabel'])
        return fig


class SettingLine:
    default = {
        'color': 'b',
        'linewidth': 2.0,
        'linestyle': 'solid',  # 'dashed'
        'marker': None,
        'markersize': 10,
        'transparency': 1,
        'label': 'variable 1'
    }

    @classmethod
    def make_params(cls, raw_data):
        warnings = list()
        params = dict()
        if raw_data['linecolor'] is not None:
            params['color'] = raw_data['linecolor']
        params['linewidth'] = cls.process_linewidth(raw_data, warnings)
        params['linestyle'] = cls.process_linestyle(raw_data, warnings)
        return params

    @classmethod
    def process_linewidth(cls, raw_data, warnings=[]):
        linewidth = raw_data.get('linewidth', None)
        try:
            linewidth = float(linewidth)
        except (TypeError, ValueError, OverflowError):
            linewidth = cls.default['linewidth']

        if linewidth <= 0:
            warnings.append(f'The linewidth is not positive: {linewidth}. Resetting to the default value')
            linewidth = 2.0
        return linewidth

    @classmethod
    def process_linestyle(cls, raw_data, warnings=[]):
        style = raw_data['linestyle']
        if style not in ['-', '--', '-.', '.']:
            warnings.append(f'Linestyle: incorrect entry: {style}')
            style = '-'
        return style

    @classmethod
    def plot(cls, fig, yvals, xmin, xmax, raw_data):
        params = cls.make_params(raw_data)
        print(f'Converted params are {params}')

        n_points = len(yvals)
        xvals = np.linspace(xmin, xmax, n_points)
        new_plot = fig.add_subplot(111)
        new_plot.plot(xvals, yvals, **params)


default_plot_parameters = {
                           'marker': None,
                           'markersize': 10,
                           'transparency': 1,

                           'isgrid': False,
                           'filename': 'plot.png'
                           }
