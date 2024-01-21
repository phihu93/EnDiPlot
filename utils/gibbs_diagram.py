import os
from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt

from utils.general import read_options


class States:
    """
    Specific states to be plotted in the diagram are defined here.

    Attributes
    ----------
    labels : list
        The labels of the states.
    kinds : list
        IM for intermediate or TS for transition state.
    lengths : list
        The lengths plotted for the state.
    values : list
        The Gibbs free energies of the states.

    Methods
    -------
    add_label()
        Adds a label of a state.
    add_kind()
        Adds a kind (IM or TS) of a state.
    add_length()
        Adds plotted length of a state.
    add_value()
        Adds Gibbs free energy of a state.
    """

    def __init__(self):
        self.labels = []
        self.kinds = []
        self.lengths = []
        self.values = []

    def add_label(self, label):
        self.labels.append(label)

    def add_kind(self, kind):
        self.kinds.append(kind)

    def add_length(self, length):
        self.lengths.append(int(length))

    def add_value(self, value):
        self.values.append(float(value))


class GibbsPlot:
    def __init__(self):
        fig = plt.figure()
        fig.set_size_inches(3.5, 2.5)
        fig.add_axes([0, 0, 1, 1])

    @staticmethod
    def define_parabola(
        x_start: int, x_end: int, y_start: float, y_max: float, y_end: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Constructs points for a parabola to indicate a transition state.

        Parameters
        ----------
        x_start : int
            x-value for starting point of parabola.
        x_end : int
            x-value for end point of parabola.
        y_start : float
            y-value for starting point of parabola.
        y_max : float
            y-value for maximum of parabola.
        y_end : float
            y-value for end point of parabola.
        """
        x_mid = (x_start + x_end) / 2
        y_mid = max(y_start + 0.01, y_max, y_end + 0.01)
        x_vals = [x_start, x_mid, x_end]
        # Construction of the first part of the parabola
        y_vals = [y_start, y_mid, y_start]
        coeff = np.polyfit(x_vals, y_vals, 2)
        x_interval_1 = np.linspace(x_start, x_mid, 50)
        y_interval_1 = np.polyval(coeff, x_interval_1)
        # Construction of the second part of the parabola
        y_vals = [y_end, y_mid, y_end]
        coeff = np.polyfit(x_vals, y_vals, 2)
        x_interval_2 = np.linspace(x_mid, x_end, 50)
        y_interval_2 = np.polyval(coeff, x_interval_2)
        # Put both parts together
        x_parabola = np.concatenate((x_interval_1, x_interval_2))
        y_parabola = np.concatenate((y_interval_1, y_interval_2))
        return x_parabola, y_parabola

    @staticmethod
    def save_figure(fontsize=8):
        plt.yticks(fontsize=fontsize)
        plt.xticks([])
        plt.ylabel("$\\mathrm{\\Delta} G$ (kJ/mol)", fontsize=fontsize)
        plt.xlabel("Reactioncoordinate", fontsize=fontsize)
        plt.savefig("gibbs_plot.pdf", bbox_inches="tight")
        plt.close()

    def plot_lines(self, plot_data, option_data, num_plot):
        counter = option_data["offset"][num_plot]
        for i, kind in enumerate(plot_data.kinds):
            x_start = counter
            counter = counter + plot_data.lengths[i]
            x_end = counter
            value = plot_data.values[i]
            if kind == "IM":
                if i > 0:
                    previous_kind = plot_data.kinds[i - 1]
                    if previous_kind == "IM":
                        previous_value = plot_data.values[i - 1]
                        plt.plot(
                            [x_start, x_start + 1],
                            [previous_value, value],
                            c=option_data["colors"][num_plot],
                            ls=":",
                        )
                        x_start += 1
                        x_end += 1
                        counter += 1
                plt.plot(
                    [x_start, x_end], [value, value], c=option_data["colors"][num_plot]
                )
            if kind == "TS":
                try:
                    previous_kind = plot_data.kinds[i - 1]
                    next_kind = plot_data.kinds[i + 1]
                    if (previous_kind != "IM") or (next_kind != "IM"):
                        raise ValueError("Transitions states have to "
                                         "embedded between two states of IM")
                except:
                    print(
                        (
                            "Transitions states have to embedded between"
                            " two states of IM"
                        )
                    )
                    exit()
                previous_value = plot_data.values[i - 1]
                next_value = plot_data.values[i + 1]
                if value < next_value or value < previous_value:
                    print(
                        "Transition state ",
                        plot_data.labels[i],
                        "is lower than intermediates!",
                    )
                x_parabola, y_parabola = self.define_parabola(
                    x_start, x_end, previous_value, value, next_value
                )
                plt.plot(x_parabola, y_parabola, c=option_data["colors"][num_plot])


def read_infiles(inf):
    if not os.path.isfile(inf):
        print("Inputfile:    " + inf + " missing")
        exit()
    else:
        print("Inputfile:    " + inf)
    plot_data = States()
    with open(inf) as fil:
        for line in fil:
            plot_data.add_length(line.split()[0])
            plot_data.add_kind(line.split()[1])
            plot_data.add_label(line.split()[2])
            plot_data.add_value(line.split()[3])
    return plot_data


def do_gibbs_diagram(option_file):
    option_data = read_options(option_file)
    do_the_plot = GibbsPlot()
    for num_plot in range(option_data["nfiles"]):
        plot_data = read_infiles(option_data["files"][num_plot])
        do_the_plot.plot_lines(plot_data, option_data, num_plot)
        # if option_data['plot_labels']:

    do_the_plot.save_figure()
