import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


class Logger:
    """Custom logger class for the application"""
    
    def __init__(self, name=__name__, log_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup console and file handlers"""
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        
        # File handler with rotation
        log_file = os.path.join(log_dir, 'app.log')
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        
        # Error file handler
        error_log_file = os.path.join(log_dir, 'error.log')
        error_handler = RotatingFileHandler(
            error_log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
    
    def debug(self, message, *args, **kwargs):
        """Log debug message"""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message, *args, **kwargs):
        """Log info message"""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        """Log warning message"""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        """Log error message"""
        self.logger.error(message, *args, **kwargs)
    
    def exception(self, message, *args, **kwargs):
        """Log exception with traceback"""
        self.logger.exception(message, *args, **kwargs)


def get_logger(name=None, log_level=None):
    """Factory function to get logger instance"""
    if name is None:
        name = __name__
    
    if log_level is None:
        # Get log level from environment or default to INFO
        log_level_str = os.getenv('LOG_LEVEL', 'INFO').upper()
        log_level = getattr(logging, log_level_str, logging.INFO)
    
    return Logger(name, log_level)


# Create default logger instance
logger = get_logger('backend')