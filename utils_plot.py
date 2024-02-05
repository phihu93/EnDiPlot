import os
from typing import Tuple, List, Dict

import numpy as np
import matplotlib.pyplot as plt

from utils_io import read_options


class States:
    """
    Specific states to be plotted in the diagram are defined here.

    Attributes
    ----------
    labels : list
        The labels of the states.
    kinds : list
        "IM" for intermediate or "TS" for transition state.
    lengths : list
        The lengths plotted for the state.
    values : list
        The energies of the states.

    Methods
    -------
    add_label()
        Adds a label of a state.
    add_kind()
        Adds a kind ("IM" or "TS") of a state.
    add_length()
        Adds plotted length of a state.
    add_value()
        Adds energy of a state.
    """

    def __init__(self) -> None:
        """
        Initializes parameters for the states.
        """
        self.labels = []
        self.kinds = []
        self.lengths = []
        self.values = []

    def add_label(self, label: str) -> None:
        """
        Adds a label of a state.
        """
        self.labels.append(label)

    def add_kind(self, kind: str) -> None:
        """
        Adds a kind ("IM" or "TS") of a state.
        """
        self.kinds.append(kind)

    def add_length(self, length: int) -> None:
        """
        Adds plotted length of a state.
        """
        self.lengths.append(length)

    def add_value(self, value: float) -> None:
        """
        Adds energy of a state.
        """
        self.values.append(value)


def plot_labels(
    element_plot_data: States, option_data: Dict, num_plot: int, y_range: List[float]
) -> None:
    """
    Plots the lines for the states.

    Parameters
    __________
    element_option_data : dict
        General data for the figure.
    plot_data : list
        General data for class States
        saved as element for each plot.
    num_plot : int
        Number of input file treated.
    y_range : list
        Interval for the y-axis used to calculate an
        offset between plotted line and label.
    """
    label_shift = (y_range[1] - y_range[0]) / 50
    counter = option_data["offset"][num_plot]
    for i, label in enumerate(element_plot_data.labels):
        x_start = counter
        counter = counter + element_plot_data.lengths[i]
        if element_plot_data.kinds[i] == "dashed":
            continue
        x_end = counter
        x_mid = (x_end + x_start) / 2
        value = element_plot_data.values[i]
        if element_plot_data.kinds[i] == "TS":
            if (
                element_plot_data.values[i - 1] > element_plot_data.values[i]
                or element_plot_data.values[i + 1] > element_plot_data.values[i]
            ):
                # Add extra sift if TS is below IM.
                value = (
                    max(
                        element_plot_data.values[i - 1], element_plot_data.values[i + 1]
                    )
                    + 0.01
                )
        y_shifted = value + label_shift
        color = option_data["colors"][num_plot]
        plt.text(
            x_mid,
            y_shifted,
            label,
            ha="left",
            color=color,
            rotation=90,
            fontsize=option_data["fontsize"],
        )


class EnergyPlot:
    """
    The energy diagram is constructed here.

    Methods
    -------
    define_parabola()
        Constructs points for a parabola to indicate a transition state.
    save_figure()
        Saves the figure.
    plot_lines()
        Plots the lines for the states.
    plot_labels()
        Plots labels for the states if plot_labels == True.
    define_figure_ranges()
        Defines y-limits.
    """

    def __init__(self) -> None:
        """
        Initializes figure.
        """
        fig, ax = plt.subplots()
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

        Returns
        -------
        np.ndarray
            x-values for the parabola.
        np.ndarray
            y-values for the parabola.
        """
        x_mid = (x_start + x_end) / 2
        y_mid = max(y_start + 0.01, y_max, y_end + 0.01)
        x_vals = [x_start, x_mid, x_end]
        # Construction of the first half of the parabola.
        y_vals = [y_start, y_mid, y_start]
        coeff = np.polyfit(x_vals, y_vals, 2)
        x_interval_1 = np.linspace(x_start, x_mid, 50)
        y_interval_1 = np.polyval(coeff, x_interval_1)
        # Construction of the second half of the parabola.
        y_vals = [y_end, y_mid, y_end]
        coeff = np.polyfit(x_vals, y_vals, 2)
        x_interval_2 = np.linspace(x_mid, x_end, 50)
        y_interval_2 = np.polyval(coeff, x_interval_2)
        # Put both halves together.
        x_parabola = np.concatenate((x_interval_1, x_interval_2))
        y_parabola = np.concatenate((y_interval_1, y_interval_2))
        return x_parabola, y_parabola

    @staticmethod
    def save_figure(y_range: List[float], option_data: Dict) -> None:
        """
        Saves the figure.

        Parameters
        __________
        y_range : list
            Interval for the y-axis to be plotted.
        option_data : dict
            General data for the figure.
        """
        plt.ylim(y_range[0], y_range[1])
        plt.yticks(fontsize=option_data["fontsize"])
        plt.xticks([])
        plt.ylabel(option_data["ylabel"], fontsize=option_data["fontsize"])
        plt.xlabel("Reaction coordinate", fontsize=option_data["fontsize"])
        plt.savefig("plot.pdf", bbox_inches="tight")
        plt.close()

    def plot_lines(
        self, element_plot_data: States, option_data: Dict, num_plot: int
    ) -> None:
        """
        Plots the lines for the states.

        Parameters
        __________
        option_data : dict
            General data for the figure.
        element_plot_data : States
            General data for class States saved as element for each plot.
        num_plot : int
            Number of input file considered.

        Raises
        ------
        ValueError
            If transitions state or dashed line is not embedded between two states of IM.
        """
        num_states = len(element_plot_data.kinds)
        counter = option_data["offset"][num_plot]
        for i, kind in enumerate(element_plot_data.kinds):
            x_start = counter
            counter = counter + element_plot_data.lengths[i]
            x_end = counter
            value = element_plot_data.values[i]
            if kind == "IM":
                # Plot line for intermediate.
                plt.plot(
                    [x_start, x_end], [value, value], c=option_data["colors"][num_plot]
                )
            if kind == "dashed":
                # Plot dashed lines between intermediates.
                if i > 0:
                    previous_kind = element_plot_data.kinds[i - 1]
                    previous_value = element_plot_data.values[i - 1]
                else:
                    raise ValueError(
                        "Dashed lines havehave to be"
                        "embedded between two states of IM"
                    )
                if i + 1 <= num_states:
                    next_kind = element_plot_data.kinds[i + 1]
                    next_value = element_plot_data.values[i + 1]
                else:
                    raise ValueError(
                        "Dashed lines havehave to be"
                        "embedded between two states of IM"
                    )
                if previous_kind != "IM" and next_kind != "IM":
                    raise ValueError(
                        "Dashed lines havehave to be"
                        "embedded between two states of IM"
                    )
                plt.plot(
                    [x_start, x_end],
                    [previous_value, next_value],
                    c=option_data["colors"][num_plot],
                    ls=":",
                )
            if kind == "TS":
                # Plot parabola for transition state.
                if i >= 1:
                    previous_kind = element_plot_data.kinds[i - 1]
                    next_kind = element_plot_data.kinds[i + 1]
                    if (previous_kind != "IM") or (next_kind != "IM"):
                        raise ValueError(
                            "Transitions states have to be"
                            "embedded between two states of IM"
                        )
                else:
                    raise ValueError(
                        "Transitions states have to be"
                        "embedded between two states of IM"
                    )
                previous_value = element_plot_data.values[i - 1]
                next_value = element_plot_data.values[i + 1]
                if value < next_value or value < previous_value:
                    print(
                        f"Transition state {element_plot_data.labels[i]} is lower than intermediates!"
                    )
                x_parabola, y_parabola = self.define_parabola(
                    x_start, x_end, previous_value, value, next_value
                )
                plt.plot(x_parabola, y_parabola, c=option_data["colors"][num_plot])

    @staticmethod
    def define_figure_ranges(
        plot_data: List, option_data: Dict
    ) -> Tuple[List[int], List[float]]:
        """
        Defines ranges within points are plotted.

        Parameters
        ----------
        plot_data : list
            General data for class States
            saved as element for each plot.
        option_data : dict
            General data for the figure.

        Returns
        -------
        list
            x-range of points.
        list
            y-range of points.
        """
        x_max = 0
        y_max = 0
        y_min = 0
        for num_plot in range(option_data["nfiles"]):
            counter = option_data["offset"][num_plot] + 1
            for i, kind in enumerate(plot_data[num_plot].kinds):
                counter = counter + plot_data[num_plot].lengths[i]
                if i > 0 and kind == "IM":
                    if plot_data[num_plot].kinds[i - 1] == "IM":
                        counter += 1
                y_max = max(y_max, plot_data[num_plot].values[i])
                y_min = min(y_min, plot_data[num_plot].values[i])
            counter += 1
            x_max = max([counter, x_max])
        x_range = [0, x_max]
        if option_data["ymin"] == 0 and option_data["ymax"] == 0:
            y_shift = (y_max - y_min) * 0.15
            y_max = y_max + y_shift
            y_min = y_min - y_shift
            y_range = [y_min, y_max]
        else:
            y_range = [option_data["ymin"], option_data["ymax"]]
        return x_range, y_range


def read_infiles(inf: str) -> States:
    """
    Reads input files for plots and saves them as States object.

    Parameters
    ----------
    inf: str
        Path to input file for plots.

    Returns
    -------
    States
        Plot data saved as States object

    Raises
    ------
    FileNotFoundError
        If input file does not exist.
    """
    if not os.path.isfile(inf):
        raise FileNotFoundError(f"Input file:\t{inf} missing")
    else:
        print(f"Input file:\t{inf}")
    element_plot_data = States()
    with open(inf) as fil:
        for line in fil:
            element_plot_data.add_length(int(line.split()[0]))
            element_plot_data.add_kind(str(line.split()[1]))
            element_plot_data.add_label(str(line.split()[2]))
            element_plot_data.add_value(float(line.split()[3]))
    return element_plot_data


def do_energy_diagram(option_file: str) -> None:
    """
    Makes the energy diagram.

    Parameters
    ----------
    option_file: str
        Path to input file for option data.
    """
    option_data = read_options(option_file)
    do_the_plot = EnergyPlot()
    plot_data = []
    for num_plot in range(option_data["nfiles"]):
        plot_data.append(read_infiles(option_data["files"][num_plot]))
    x_range, y_range = do_the_plot.define_figure_ranges(plot_data, option_data)
    for num_plot in range(option_data["nfiles"]):
        do_the_plot.plot_lines(plot_data[num_plot], option_data, num_plot)
        if option_data["plot_labels"]:
            plot_labels(plot_data[num_plot], option_data, num_plot, y_range)
    do_the_plot.save_figure(y_range, option_data)
