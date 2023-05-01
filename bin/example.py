import set_python_path
import random

from simmanager import Paths
from utils.hydrashim import hydra
from utils.hydrashim import DictConfig
from utils.basicutils import loggingext_decorator, simmanager_context_decorator
from utils.basicutils import getFrameDir

import logging

script_dir = getFrameDir()

def simulate_dice_rolls(n_rolls, n_sides, seed):
    dice_rolls_logger = logging.getLogger("example.dice_rolls_function")
    random.seed(seed)
    dice_rolls_logger.info(f"Simulating {n_rolls} dice rolls with {n_sides} sides (seed: {seed})")
    return [random.randint(1, n_sides) for _ in range(n_rolls)]

@hydra.main(config_path=f'{script_dir}/../config', config_name='config')
@simmanager_context_decorator
@loggingext_decorator
def main(cfg: DictConfig, output_paths: Paths):
    main_logger = logging.getLogger("example.main_function")
    
    main_logger.debug("Starting simulation")
    rolls = simulate_dice_rolls(cfg.n_rolls, cfg.n_sides, cfg.seed)
    
    main_logger.debug("Saving simulation data")
    with open(output_paths.simulation_path / "dice_rolls.txt", "w") as f:
        f.write("\n".join(map(str, rolls)))
    
    main_logger.debug("Calculating average roll")
    avg_roll = sum(rolls) / len(rolls)
    main_logger.info(f"Average roll: {avg_roll:.2f}")

if __name__ == '__main__':
    main()
