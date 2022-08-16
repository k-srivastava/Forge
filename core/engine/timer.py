"""
Basic timer in Forge.
"""
import dataclasses
import timeit


@dataclasses.dataclass(slots=True)
class Timer:
    """
    Forge's basic timer using real-world time data as opposed to an in-built game timer for greater accuracy.
    """
    rounding: int = 2
    _start: float | None = None

    def start(self) -> None:
        """
        Start the timer.
        """
        self._start = timeit.default_timer()

    def stop(self) -> None:
        """
        Stop the timer.
        """
        self._start = None

    def reset(self) -> None:
        """
        Reset the timer; essentially start it over again.
        """
        self._start = timeit.default_timer()

    def time(self) -> float:
        """
        Get the elapsed time since the timer was started in seconds. Also round the elapsed time to a specified
        precision.

        :return: Elapsed time since the timer was started.
        :rtype: float

        :raises RuntimeError: A stopped timer cannot output the elapsed time.
        """
        if self._start is not None:
            return round((timeit.default_timer() - self._start), self.rounding)

        raise RuntimeError('Cannot get elapsed time from a stopped timer.')
