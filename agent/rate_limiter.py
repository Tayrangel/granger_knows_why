import time
from functools import wraps
from collections import defaultdict
from typing import Callable, Any, Dict, List
from agent.config import RATE_LIMIT_CALLS, RATE_LIMIT_PERIOD


class RateLimiter:
    """
    Simple in-memory rate limiter using sliding window algorithm.
    
    Usage:
        limiter = RateLimiter(calls=10, period=3600)  # 10 calls per hour
        
        @limiter
        def expensive_api_call():
            ...
    """
    
    def __init__(self, calls: int, period: int) -> None:
        """
        Initialize rate limiter.
        
        Args:
            calls: Number of calls allowed
            period: Time period in seconds (e.g., 3600 for 1 hour)
        """
        self.calls = calls
        self.period = period
        self.request_times: Dict[str, List[float]] = defaultdict(list)
    
    def __call__(self, func: Callable) -> Callable:
        """Apply rate limiting as a decorator."""
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Extract user_id from kwargs, default to 'anonymous'
            user_id = kwargs.pop('user_id', 'anonymous')
            now = time.time()
            
            # Clean up old requests outside the time window
            self.request_times[user_id] = [
                request_time for request_time in self.request_times[user_id]
                if now - request_time < self.period
            ]
            
            # Check if rate limit is exceeded
            if len(self.request_times[user_id]) >= self.calls:
                raise RateLimitExceeded(
                    f"Rate limit exceeded: {self.calls} calls per {self.period} seconds"
                )
            
            # Record this request
            self.request_times[user_id].append(now)
            
            # Call the original function
            return func(*args, user_id=user_id, **kwargs)
        
        return wrapper
    
    def is_allowed(self, user_id: str = 'anonymous') -> bool:
        """
        Check if a user is allowed to make a request without executing it.
        
        Args:
            user_id: User identifier
            
        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()
        
        # Clean up old requests
        self.request_times[user_id] = [
            request_time for request_time in self.request_times[user_id]
            if now - request_time < self.period
        ]
        
        return len(self.request_times[user_id]) < self.calls
    
    def get_remaining(self, user_id: str = 'anonymous') -> int:
        """
        Get remaining calls for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Number of remaining calls
        """
        now = time.time()
        
        # Clean up old requests
        self.request_times[user_id] = [
            request_time for request_time in self.request_times[user_id]
            if now - request_time < self.period
        ]
        
        return max(0, self.calls - len(self.request_times[user_id]))
    
    def reset(self, user_id: str = 'anonymous') -> None:
        """
        Reset rate limit for a user.
        
        Args:
            user_id: User identifier
        """
        if user_id in self.request_times:
            self.request_times[user_id] = []


class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded."""
    pass


# Global rate limiter for API calls
api_rate_limiter = RateLimiter(calls=RATE_LIMIT_CALLS, period=RATE_LIMIT_PERIOD)
