import argparse
import os

from utils.gibbs_diagram import do_gibbs_diagram


def main(config):
    options_file = config.options
    if not os.path.isfile(options_file):
        raise FileNotFoundError(options_file)
    else:
        print(f"Optionfile:   {options_file}")
    do_gibbs_diagram(options_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="test.py", description="Try some stuff")
    parser.add_argument(
        "-o", "--options", help="Settings for plotting", default="opt.inp", type=str
    )
    config = parser.parse_args()
    main(config)
