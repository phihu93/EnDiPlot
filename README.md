
# EnDiPlot

[![](https://img.shields.io/badge/Python-3.8-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The `EnDiPlot` Python package plots energy diagrams for reaction mechanisms using `matplotlib`.
An example of a plot is given in folder *data*. 
The program is run by: `python chemplots -o <path/to/option/data/file>`


### Required input files

- File with general data used for the plot (*option data file*).

- Files containing specific values to be plotted for a reaction path (*plot data file*).
 
#### Option data file

Keywords are indicated with <*keyword*. 
Corresponding information has to be given in following lines using a single space as the first character (see example in folder *data*).
Following keywords have to be specified:

- `nfiles`: Number of plot data files.
- `files`: Names of plot data files.
- `offset`: Offsets in the plot for a specific path.
- `colors`: Colors as available in `matplotlib` used for the plot of a given path.

Following keywords can be specified optionally:

- `plot_titles`: True if legend is required in the plot. Default: False
- `titles`: Title plotted for the legend (only if `plot_legend` is True).
- `plot_labels`: True if labels for the states are required in the plot. Default = False.
- `labels`: Labels plotted for the states in the plot (only if `plot_labels` is True).
- `fontsize`: Fontsize for axis label, tick labels, legend, and labels for states. Default = 7.
- `ymin`: Minimum plotted for y-axis.
- `ymax`: Maximum plotted for y-axis.
- `ylabel`: Label for y axis. Default = *$\\\\mathrm{\\\\Delta} G$ (kJ/mol)*

#### Plot data file

Several reaction paths, each saved in a separate file as specified for *files* in the option data file, can be plotted.
Data for each state to be plotted has to be defined in one line containing four elements separated by spaces:

1. `length`: An integer which defines the length of the plotted state.
2. `kind`: Defines the kind of state, i.e., "IM" for an intermediate and "TS" for a transition state.
3. `label`: Label of the state, which is plotted, if `plot_label` is True in option data file.
4. `value`: A float value where the state is plotted.

If `kind` is dashed, a dashed line is plotted between its preceding and following intermediate. 
For dashed lines, `label` and `value` are ignored.