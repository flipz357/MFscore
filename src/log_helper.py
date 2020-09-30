import logging

def get_logger(name="Logger"
        , level=50
        , format='%(asctime)s:\t%(name)s:\t%(levelname)s:\t%(message)s'):
    logger = logging.getLogger(name=name)
    logger.setLevel(level=level)
    logging.basicConfig(format=format)
    return logger
