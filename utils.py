import logging
import logging.config
import time
import warnings
import yaml


def setup_logger(
    logger_name: str, log_config_file: str, log_file: str = "file1.log"
) -> logging.Logger:
    if not log_config_file:
        raise ValueError("Please provide a log configuration file path.")
    
    with open(log_config_file, "r") as f:
        config = yaml.safe_load(f.read())

        # set the filename for the RotatingFileHandler
        config["handlers"]["file"]["filename"] = log_file

        # apply logging config to logging
        logging.config.dictConfig(config)

        if logger_name not in config["loggers"]:
            warnings.warn(
                "Beware! The logger name you provided does not match any logger defined in the logging config file. "
                f"({list(config['loggers'].keys())}). Using the root logger."
            )
            logger_name = "root"

        return logging.getLogger(logger_name)


def timer(logger=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            t1 = time.perf_counter()
            result = func(*args, **kwargs)
            t2 = time.perf_counter()
            execution_time = t2 -t1
            if logger:
                logger.info(f"Execution time of '{func.__name__}': {execution_time:.2f} seconds")
            else:
                print(f"Execution time of '{func.__name__}': {execution_time:.2f} seconds.")
            return result
        return wrapper
    return decorator
