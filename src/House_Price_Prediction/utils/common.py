import os
from box.exception import BoxValueError
import yaml
import sys
import logging
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64



def logger():
    logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

    log_dir = "logs"
    log_filepath = os.path.join(log_dir, "running_logs.log")
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(level=logging.INFO, format=logging_str, handlers=[logging.FileHandler(log_filepath), logging.StreamHandler(sys.stdout)])
    logger = logging.getLogger("House_Price_Prediction")
    return logger

@ensure_annotations
def read_yaml(path_to_yaml: str) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input
    
    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try: 
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        verbose (bool, optional): ignore if multiple dirs is to be created. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")
            
@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"json file saved at: {path}")
    