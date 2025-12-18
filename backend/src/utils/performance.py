"""
Performance monitoring utilities for tracking system performance during transition period.
"""
import time
import functools
from typing import Callable, Any
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """
    Performance monitoring during transition period (PERF-003)
    """
    def __init__(self):
        self.metrics = {}

    def time_function(self, name: str = None):
        """
        Decorator to time function execution
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.time()
                    execution_time = end_time - start_time

                    # Log performance metrics
                    func_name = name or func.__name__
                    logger.info(f"Performance: {func_name} executed in {execution_time:.4f}s")

                    # Store metrics for monitoring
                    if func_name not in self.metrics:
                        self.metrics[func_name] = []
                    self.metrics[func_name].append(execution_time)

                    # Alert if performance degrades beyond threshold
                    if execution_time > 1.0:  # 1 second threshold
                        logger.warning(f"Performance alert: {func_name} took {execution_time:.4f}s (threshold: 1.0s)")
            return wrapper
        return decorator

    def get_average_execution_time(self, func_name: str) -> float:
        """Get average execution time for a function"""
        if func_name in self.metrics and self.metrics[func_name]:
            return sum(self.metrics[func_name]) / len(self.metrics[func_name])
        return 0.0

    def get_performance_report(self) -> dict:
        """Get comprehensive performance report"""
        report = {}
        for func_name, times in self.metrics.items():
            report[func_name] = {
                'count': len(times),
                'average': sum(times) / len(times),
                'min': min(times),
                'max': max(times),
                'total': sum(times)
            }
        return report

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

# Convenience decorators
time_api_call = performance_monitor.time_function
time_db_operation = performance_monitor.time_function
time_service_call = performance_monitor.time_function