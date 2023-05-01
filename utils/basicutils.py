"""
Contains all miscellaneous utils that make the use of python just that much
syntactically sweeter.

Not all of them are used as this is wisdom born from a lot of projects. Oh and this
file is MIT licensed if anyone wants to use something here.
"""

import os
from os.path import join as opj
import inspect
import functools

from contextlib import ExitStack

from utils.hydrashim import hydra
from utils.hydrashim import DictConfig, OmegaConf

from simmanager import SimManager, Paths
from loggingext.logsetup import create_shared_logger_data, configure_loggers

float_re = r'-?\d+(?:\.\d+)?(?:[eE]-?\d+)?'


def get_shared_logger_data(loggercfg: DictConfig):
    logger_names = []
    log_levels = []
    log_to_consoles = []

    if isinstance(loggercfg, list):
        loggercfg_iter = loggercfg
    else:
        loggercfg_iter = loggercfg.values()
    for cfg in loggercfg_iter:
        logger_names.append(cfg.name)
        log_levels.append(cfg.get('level', 'INFO'))
        log_to_consoles.append(cfg.get('to_stdout', True))

    return logger_names, log_levels, log_to_consoles


def loggingext_decorator(task_func):
    @functools.wraps(task_func)
    def wrapper(cfg: DictConfig, output_paths: Paths):

        logger_names, log_levels, log_to_consoles = get_shared_logger_data(cfg.get('loggers', {}))
        create_shared_logger_data(logger_names, log_levels, log_to_consoles,
                                  sim_name=cfg.sim_name,
                                  log_directory=output_paths.log_path)
        configure_loggers()
        return task_func(cfg, output_paths)
    return wrapper


def simmanager_context_decorator(task_func):

    @functools.wraps(task_func)
    def wrapper(cfg: DictConfig):
        OmegaConf.resolve(cfg)
        root_dir = os.environ['RESULTS_ROOT_DIR']
        sim_name = cfg.sim_name
        output_dir_name = cfg.output_dir_name

        with SimManager(sim_name, root_dir, output_dir_name, **cfg.sim_man) as sim_man:
            with open(opj(sim_man.paths.data_path, 'sim_config.yaml'), 'w') as fout:
                fout.write(OmegaConf.to_yaml(cfg))
            with ExitStack() as E:
                if hasattr(simmanager_context_decorator, 'debug') and simmanager_context_decorator.debug:
                    import ipdb
                    E.enter_context(ipdb.launch_ipdb_on_exception())
                return task_func(cfg, sim_man.paths)
    return wrapper


def getFrameDir():
    """
    Gets the direcctory of the script calling this function.
    """
    CurrentFrameStack = inspect.stack()
    if len(CurrentFrameStack) > 1:
        ParentFrame = CurrentFrameStack[1][0]
        FrameFileName = inspect.getframeinfo(ParentFrame).filename
        FrameDir = os.path.dirname(os.path.abspath(FrameFileName))
    else:
        FrameDir = None

    return FrameDir
