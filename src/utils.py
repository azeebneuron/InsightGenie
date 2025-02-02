import streamlit as st
import functools
import time
from typing import Callable, Any

class CustomException(Exception):
    """Custom exception class for application-specific errors."""
    pass

def log_execution_time(func: Callable) -> Callable:
    """
    Decorator to log the execution time of a function.
    
    Args:
        func (Callable): The function to be decorated.
    
    Returns:
        Callable: The decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        st.write(f"Execution time of {func.__name__}: {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def cache_data(func: Callable) -> Callable:
    """
    Decorator to cache the results of a function using Streamlit's caching mechanism.
    
    Args:
        func (Callable): The function to be decorated.
    
    Returns:
        Callable: The decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        return st.cache_data(func)(*args, **kwargs)
    return wrapper

def display_error(message: str):
    """
    Display a user-friendly error message in the Streamlit app.
    
    Args:
        message (str): The error message to display.
    """
    st.error(f"Error: {message}")

# Example usage
# if __name__ == "__main__":
#     @log_execution_time
#     def example_function():
#         time.sleep(2)
#         return "Done"

#     st.write(example_function())