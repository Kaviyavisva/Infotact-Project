"""
Enterprise-grade logging configuration and utilities.
"""
import sys
import time
import functools
from loguru import logger

from config import settings

def setup_logger():
    """
    Configures loguru to log to both stdout and a rolling log file.
    """
    logger.remove() # Remove default handler
    
    # Console output for active development
    logger.add(
        sys.stdout, 
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # File output for persistent debugging
    log_path = settings.LOGS_DIR / "vector_store.log"
    logger.add(
        str(log_path),
        rotation="10 MB",
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        backtrace=True,
        diagnose=True
    )
    
    logger.info("Enterprise logging configured successfully.")
    return logger

# Initialize logging globally when this module is imported
setup_logger()

def log_execution_time(func):
    """
    Decorator to log the execution time of operations.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.debug(f"Starting execution of {func.__name__}...")
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"Completed {func.__name__} in {duration:.4f} seconds.")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Failed {func.__name__} after {duration:.4f} seconds with error: {e}")
            raise
    return wrapper
