import os
import json
import matplotlib.pyplot as plt
from collections import Counter

import argparse
from simmanager import Paths


def analysis_main(output_paths: Paths) -> None:
    # Load dice roll data
    with open(os.path.join(output_paths.simulation_path, "dice_rolls.json"), "r") as f:
        dice_rolls = json.load(f)

    # Calculate histogram
    histogram = Counter(dice_rolls)

    # Plot histogram
    plt.bar(histogram.keys(), histogram.values())
    plt.xlabel("Dice Roll")
    plt.ylabel("Frequency")
    plt.title("Dice Roll Histogram")

    # Save plot in the results directory
    plt.savefig(os.path.join(output_paths.results_path, "dice_roll_histogram.png"))
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dice Roll Simulation Analysis")
    parser.add_argument("--dir", type=str, required=True, help="Simulation directory path")
    args = parser.parse_args()

    output_dir_path = args.dir
    output_paths = Paths(output_dir_path)

    analysis_main(output_paths)
