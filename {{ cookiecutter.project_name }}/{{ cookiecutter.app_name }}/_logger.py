import logging

loggers = {}

def setup_custom_logger(name):
    """
    Create a logger with a certain name and level
    """
    global loggers

    if loggers.get(name):
        return loggers.get(name)

    formatter = logging.Formatter(
        fmt='%(levelname)s: %(message)s'
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # \033[1;30m - black
    # \033[1;31m - red
    # \033[1;32m - green
    # \033[1;33m - yellow
    # \033[1;34m - blue
    # \033[1;35m - magenta
    # \033[1;36m - cyan
    # \033[1;37m - white

    logging.addLevelName(logging.CRITICAL, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.CRITICAL))
    logging.addLevelName(logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
    logging.addLevelName(logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
    logging.addLevelName(logging.INFO, "\033[1;34m%s\033[1;0m" % logging.getLevelName(logging.INFO))
    logging.addLevelName(logging.DEBUG, "\033[1;35m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))

    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)

    # if (logger.hasHandlers()):
    #     logger.handlers.clear()
    if logger.handlers:
        logger.handlers = []
    logger.addHandler(handler)
    loggers.update(dict(name=logger))

    return logger
