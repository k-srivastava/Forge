"""
Creation, retrieval, posting and deletion of events using Forge's custom event management system.
"""
from __future__ import annotations

import dataclasses
import typing

_INTERNAL_EVENT_NAMES: list[str] = []
_EVENTS: dict[str, Event] = {}


@dataclasses.dataclass(slots=True)
class Event:
    """
    Forge's basic but sufficient event system for both internal and developer use.
    """
    name: str
    _subscribers: dict[typing.Callable[[typing.Any, ...], None],
                       tuple[typing.Any, ...]] = dataclasses.field(default_factory=dict)

    def __post_init__(self) -> None:
        """
        Check whether the supplied event name is unique and not taken by another existing or internal event.

        :raises ValueError: All event names must be unique.
        """
        if self.name in _INTERNAL_EVENT_NAMES:
            raise ValueError(f'Cannot create event: {self.name}. An internal event of the same name already exists.')

        for event_name in _EVENTS:
            if event_name == self.name:
                raise ValueError(f'Cannot create two events of the same name: {self.name}.')

        _EVENTS[self.name] = self

    def __iadd__(self, subscriber: tuple[typing.Callable[[typing.Any], None], tuple[typing.Any, ...]]) -> Event:
        """
        Register a new function to the event as a tuple of a callable and its arguments.

        :param subscriber: Function and its arguments to be registered to the event.
        :type subscriber: tuple[Callable[Any, None], tuple[Any, ...]]

        :return: The event to which the function is registered; used internally by Python.
        :rtype: Event

        :raises ValueError: All functions registered to the event must be unique.
        """
        function: typing.Callable[[typing.Any], None] = subscriber[0]
        arguments: tuple[typing.Any, ...] = subscriber[1]

        if function in self._subscribers:
            raise ValueError(f'Function {function.__name__} is already subscribed to the event.')

        self._subscribers[function] = arguments

        return self

    def __isub__(self, function: typing.Callable) -> Event:
        """
        Deregister an existing function to the event.

        :param function: Function to be deregistered from the event.
        :type function: Callable

        :return: THe event to which the function was registered; used internally by Python.
        :rtype: Event

        :raises ValueError: A function that was never registered cannot be deregistered.
        """
        if function not in self._subscribers:
            raise ValueError(f'Function {function.__name__} never subscribed to the event; cannot be removed.')

        self._subscribers.pop(function)

        return self

    def __repr__(self) -> str:
        return f'Event -> name: {self.name}, subscriber count: {len(self._subscribers)}'

    def __str__(self) -> str:
        return f'Forge Event -> name {self.name}, subscribers: {self._subscribers.keys()}'

    def post(self) -> None:
        """
        Post the event that calls all of its subscriber functions with their respective arguments. If an exception
        occurs when calling a subscriber function, it is ignored and printed to the console.
        """
        for function, arguments in self._subscribers.items():
            try:
                function(*arguments)

            except Exception as e:
                print(f'Execution of {function.__name__} led to an exception.\n{e}')


def get_event(event_name: str) -> Event:
    """
    Get a registered event from the event dictionary. Acts as an abstraction over the package-protected dictionary.
    Also does not allow getting an internal event.

    :param event_name: Name of the event to retrieve.
    :type event_name: str

    :return: Event from the dictionary with the same name.
    :rtype: Event

    :raises ValueError: Internal events cannot be retrieved.
    :raises KeyError: Event must be present in the event dictionary to retrieve.
    """
    if event_name in _INTERNAL_EVENT_NAMES:
        raise ValueError(f'Event named: {event_name} is an internal event and cannot be retrieved.')

    if event_name not in _EVENTS:
        raise KeyError(f'Event named: {event_name} has not been registered as an event and cannot be retrieved.')

    return _EVENTS[event_name]


def delete_event(event_name: str) -> None:
    """
    Delete a registered event from the event dictionary. Acts as an abstraction over the package-protected dictionary.
    Also does not allow deletion of an internal event.

    :param event_name: Name of the event to delete.
    :type event_name: str

    :raises ValueError: Internal events cannot be deleted.
    :raises KeyError: Event must be present in the event dictionary to delete.
    """
    if event_name in _INTERNAL_EVENT_NAMES:
        raise ValueError(f'Event named: {event_name} is an internal event and cannot be deleted.')

    if event_name not in _EVENTS:
        raise KeyError(f'Event named: {event_name} has not been registered as an event and cannot be deleted.')

    _EVENTS.pop(event_name)
