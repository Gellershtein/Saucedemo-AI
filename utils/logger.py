import logging
import sys
from functools import wraps
import json

def setup_logger():
    """
    Настраивает и возвращает логгер.
    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler("test_run.log"),
                                  logging.StreamHandler(sys.stdout)])
    return logging.getLogger(__name__)

logger = setup_logger()

def log_decorator(func):
    """
    Декоратор для логирования вызова функции, ее аргументов и результата.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # args[0] is 'self'
        class_name = args[0].__class__.__name__
        method_name = func.__name__
        
        logger.debug(f"Entering: {class_name}.{method_name}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Exiting: {class_name}.{method_name}, Result: {result}")
            return result
        except Exception as e:
            logger.error(f"Exception in {class_name}.{method_name}: {e}", exc_info=True)
            raise
    return wrapper
