"""
Structured logging module for Granger Knows Why.
Provides JSON-formatted logging for production debugging and monitoring.
"""

import logging
import json
import time
from datetime import datetime
from typing import Any, Dict, Optional
from functools import wraps
from agent.config import LOG_LEVEL

# Configure JSON logging
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(message)s'
)

logger = logging.getLogger(__name__)


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage()
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields if provided
        if hasattr(record, 'extra_fields'):
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data, default=str)


# Apply JSON formatter to all handlers
for handler in logger.handlers:
    handler.setFormatter(JSONFormatter())

# Ensure we have at least one handler
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)


def log_analysis(
    user_input: str,
    response: str,
    duration_ms: float,
    status: str,
    error: Optional[str] = None
) -> None:
    """
    Log an analysis request with metrics.
    
    Args:
        user_input: The user's input query
        response: The agent's response
        duration_ms: Total duration in milliseconds
        status: 'success' or 'error'
        error: Error message if status is 'error'
    """
    extra = {
        'event': 'analysis_request',
        'input_length': len(user_input),
        'response_length': len(response),
        'duration_ms': round(duration_ms, 2),
        'status': status
    }
    
    if error:
        extra['error'] = error
        logger.error(error, extra={'extra_fields': extra})
    else:
        logger.info('Analysis request completed', extra={'extra_fields': extra})


def log_tool_call(
    tool_name: str,
    duration_ms: float,
    result_length: int,
    status: str,
    error: Optional[str] = None
) -> None:
    """
    Log a tool call with metrics.
    
    Args:
        tool_name: Name of the tool that was called
        duration_ms: Duration of tool execution in milliseconds
        result_length: Length of the result returned
        status: 'success' or 'error'
        error: Error message if status is 'error'
    """
    extra = {
        'event': 'tool_call',
        'tool': tool_name,
        'duration_ms': round(duration_ms, 2),
        'result_length': result_length,
        'status': status
    }
    
    if error:
        extra['error'] = error
        logger.error(f'Tool call failed: {tool_name}', extra={'extra_fields': extra})
    else:
        logger.info(f'Tool call succeeded: {tool_name}', extra={'extra_fields': extra})


def log_context_load(
    duration_ms: float,
    status: str,
    error: Optional[str] = None
) -> None:
    """
    Log context loading from database.
    
    Args:
        duration_ms: Duration of context loading in milliseconds
        status: 'success' or 'error'
        error: Error message if status is 'error'
    """
    extra = {
        'event': 'context_load',
        'duration_ms': round(duration_ms, 2),
        'status': status
    }
    
    if error:
        extra['error'] = error
        logger.warning(f'Context load failed: {error}', extra={'extra_fields': extra})
    else:
        logger.info('Context loaded from database', extra={'extra_fields': extra})


def timing_decorator(func):
    """
    Decorator to automatically log function execution time.
    
    Usage:
        @timing_decorator
        def my_function():
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration_ms = (time.time() - start_time) * 1000
            extra = {
                'event': 'function_call',
                'function': func.__name__,
                'duration_ms': round(duration_ms, 2),
                'status': 'success'
            }
            logger.info(f'Function {func.__name__} executed', extra={'extra_fields': extra})
            return result
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            extra = {
                'event': 'function_call',
                'function': func.__name__,
                'duration_ms': round(duration_ms, 2),
                'status': 'error',
                'error': str(e)
            }
            logger.error(f'Function {func.__name__} failed', extra={'extra_fields': extra})
            raise
    
    return wrapper
