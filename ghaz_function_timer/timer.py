"""
file_name = timer.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/29/2023
Description: A file used to time functions
Edit Log:
07/29/2023
    - Created timing decorator class logic
07/30/2023
    - Documented code
    - Added timing context manger logic
"""

# STANDARD LIBRARY IMPORTS
from time import time
from typing import Any, Optional, cast

# THIRD PARTY LIBRARY IMPORTS
from stringcolor import cs as color

# LOCAL LIBRARY IMPORTS


class Timer:
    """
    A decorator class for measuring the execution time of a function.

    NOTE:
        TO update the total_time attribute you must add the @classmethod decorator
    """

    total_time: float = time()

    def __init__(self, print_time=False, print_response=False):
        """
        Initialize an instance of the Timer class.

        Args:
            print_time (bool, optional):
                Indicates whether to print the  execution time of the function.
                Defaults to False.
            print_response (bool, optional):
                Indicates whether to print the response of the function.
                Defaults to False.
        """

        self.print_time: bool = print_time
        self.print_response: bool = print_response

        self.start_time = None

    def __enter__(self) -> "Timer":
        """Context manager enter method that returns the Timer instance.

        Returns:
            Timer: The Timer instance itself.
        """
        self.start_time = time()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager exit method to calculate and print the total execution time.

        Args:
            exc_type:
                The type of exception (if any) raised in the with block.
            exc_val:
                The exception value (if any) raised in the with block.
            exc_tb:
                The traceback object (if any) raised in the with block.
        """

        self.__time_function__()

    def __call__(self, func):
        """
        Callable method to decorate a function with execution time measurement.

        Args:
            func `callable`:
                The function to be decorated.

        Returns:
            `callable`:
                The decorated function.
        """

        def wrapper(*args: Any, **kwargs: Any):
            """
            Wrapper function that measures the execution time and calls the decorated function.

            Args:
                *args:
                    Variable length argument list.
                **kwargs:
                    Arbitrary keyword arguments.

            Returns:
                `any`:
                    The result of the decorated function call.
            """
            self.start_time = time()
            response: Any = func(*args, **kwargs)

            if self.print_response:
                print(response)

            self.__time_function__(function_name=func.__name__)

            return response

        return wrapper

    def __time_function__(self, function_name: Optional[str] = None) -> None:
        """
        Calculate and return the execution time of a function.

        Returns:
            `float` :
                The execution time in seconds.
        """

        if not self.total_time:
            self.total_time = 0

        execution_time = round(time() - cast(float, self.start_time), 4)

        if self.print_time:
            self.print_and_format_time(
                "Execution time: ", execution_time, function_name
            )

    def get_total_time(self) -> float:
        """
        Calculate and return the total time.

        Returns:
            `float`: The total time in seconds.
        """

        return round(time() - self.total_time, 4)

    def print_and_format_time(
        self,
        title_string: str,
        p_time: Optional[float] = None,
        function_name: Optional[str] = None,
    ) -> None:
        """
        Prints time in a formatted way.
        """
        extra_line: bool = p_time is not None

        if not p_time:
            p_time = self.get_total_time()

        function_name_string = (
            f"({color('Function:', 'silver')} {color(f'{function_name}', 'gold2')})"
            if function_name
            else ""
        )
        title_string = color(title_string, "dodgerblue")

        full_title_string: str = (
            f"{function_name_string} {title_string}"
            if function_name_string
            else title_string
        )
        time_string: str = f"{color(f'{round(p_time, 4)}', 'green')} seconds".rstrip()

        print(f"{full_title_string:<80} {time_string:>30}")

        if extra_line:
            print()
