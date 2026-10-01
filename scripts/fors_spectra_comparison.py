"""Plot and compare FORS spectra of pigments and binders, imported as csv files. 
The csv files are expected to have at least two columns: 
the last would be the reflectance intensity (y-axis), the penultimate would be the wavelength (x-axis)."""

import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="plot and compare csv FORS spectra.")

    parser.add_argument("files", nargs="+", type=Path, help="csv file to plot")

    parser.add_argument("--save", type=Path, help="to save to obtained plot")

    parser.add_argument("--no-legend", action="store_true", help="to hide the legend")

    args = parser.parse_args()

    plt.figure(figsize=(10, 6))

    for file in args.files:

        if not file.exists():
            print(f"error: could not find the file {file}")
            continue

        try:
        # csv files are not expected to have a header
            try:
                data = pd.read_csv(
                    file,
                    header=None,
                    sep=r"[\t,]+",
                    engine="python",
                    skipinitialspace=True,
                    encoding="utf-8")
            except UnicodeDecodeError:
                data = pd.read_csv(
                    file,
                    header=None,
                    sep=r"[\t,]+",
                    engine="python",
                    skipinitialspace=True,
                    encoding="utf-16")

            if data.shape[1] < 2:
                print(f"error: skipping {file} as it has less than 2 columns")
                continue

            x = pd.to_numeric(data.iloc[:, -2], errors="raise")
            y = pd.to_numeric(data.iloc[:, -1], errors="raise")

            plt.plot(x, y, label=file.stem)

        except (pd.errors.EmptyDataError, pd.errors.ParserError, ValueError) as error:
            print(f"error while reading {file}:{error}")
            continue

    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Reflectance")
    plt.grid(True)

    if not args.no_legend:
        plt.legend()

    plt.tight_layout()

    if args.save:
        plt.savefig(args.save, dpi=300, bbox_inches="tight")
        print(f"saved plot to {args.save}")

    plt.show()

if __name__ == "__main__":
    main()
