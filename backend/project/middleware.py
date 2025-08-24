from flask import request, g
import time
from project.logger import get_logger

logger = get_logger('middleware')


def setup_request_logging(app):
    """Setup request logging middleware"""
    
    @app.before_request
    def before_request():
        """Log request start and store start time"""
        g.start_time = time.time()
        logger.info(f"Request started: {request.method} {request.url}")
        
        # Log request headers in debug mode
        if app.config.get('LOG_LEVEL') == 10:  # DEBUG level
            logger.debug(f"Request headers: {dict(request.headers)}")
            if request.is_json and request.data and request.get_json():
                # Don't log sensitive data like passwords
                data = request.get_json()
                if 'password' in data:
                    data = {k: '***' if k == 'password' else v for k, v in data.items()}
                logger.debug(f"Request JSON: {data}")
    
    @app.after_request
    def after_request(response):
        """Log request completion"""
        duration = time.time() - g.get('start_time', time.time())
        
        # Log response
        logger.info(
            f"Request completed: {request.method} {request.url} - "
            f"Status: {response.status_code} - Duration: {duration:.3f}s"
        )
        
        # Log response data in debug mode (but not for large responses)
        if app.config.get('LOG_LEVEL') == 10 and response.content_length and response.content_length < 1000:
            logger.debug(f"Response: {response.get_data(as_text=True)}")
        
        return response
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Log unhandled exceptions"""
        logger.exception(f"Unhandled exception in {request.method} {request.url}: {str(e)}")
        # Re-raise the exception to let Flask handle it normally
        raise e