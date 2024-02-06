import argparse
import os

from endiplot.utils_plot import do_energy_diagram


def main(config: argparse.Namespace) -> None:
    """
    Makes the energy diagram.

    Parameters
    ----------
    config : argparse.Namespace
        Configuration.
    """
    options_file = config.options
    if not os.path.isfile(options_file):
        raise FileNotFoundError(options_file)
    else:
        print(f"Optionfile:\t{options_file}")
    do_energy_diagram(options_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="test.py", description="Try some stuff")
    parser.add_argument(
        "-o", "--options", help="Settings for plotting", default="opt.inp", type=str
    )
    config = parser.parse_args()
    main(config)
