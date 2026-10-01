"""Plot one or more Raman spectra obtained as txt files."""

import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def main():
    """Take txt files from terminal with argparse and plot them"""
    parser = argparse.ArgumentParser(description="Plot Raman spectra")

    # input file
    parser.add_argument("-f", "--files", nargs="+", required=True,
                        help="Enter one or more txt file paths")

    # output file
    parser.add_argument("-o", "--output", default=None,
                        help="Enter a file name to save the plot (optional)")

    args = parser.parse_args()
    plt.figure(figsize=(10, 6))

    # read and plot files in the same figure
    for file in args.files:
        try:
            data = np.loadtxt(file, skiprows=1)
        except FileNotFoundError:
            print(f"File not found: '{file}'")
            continue
        except ValueError:
            print(f"Invalid data in'{file}'")
            continue

        # Raman shift on the x-axis and scattering intensity on the y-axis
        raman_shift = data[:, 0]
        intensity = data[:, 1]

        # get file name and create a clear legend label
        file_name = Path(file).stem
        sample = file_name.split("_")[0]
        material = file_name.rsplit("_", 1)[1]
        label = f"{sample}_{material}"

        # plot data
        plt.plot(raman_shift, intensity, label=label)

    # add axes and label
    plt.xlabel(r"Raman shift (cm$^{-1}$)")
    plt.ylabel("Raman intensity")
    plt.legend()

    plt.grid(True)
    plt.tight_layout()

    # save the plot if specified
    if args.output is not None:
        output = args.output
        if not output.lower().endswith(".png"):
            output += ".png"
        plt.savefig( output, dpi=300, bbox_inches="tight", format="png" )
        print(f"Plot saved as: '{output}'")
    plt.show()

if __name__ == "__main__":
    main()
