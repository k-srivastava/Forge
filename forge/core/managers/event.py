"""
Creation, retrieval, posting and deletion of events using Forge's custom event management system.
"""
from __future__ import annotations

import dataclasses
import typing
import warnings

import attrs

import forge.core.utils.id

_INTERNAL_EVENT_NAMES: list[str] = []
_EVENTS: dict[int, Event] = {}
EVENT_IDS: dict[str, int] = {}


@dataclasses.dataclass(slots=True)
class Event:
    """
    Forge's basic but sufficient event system for both internal and developer use.
    """
    name: str = attrs.field(on_setattr=attrs.setters.frozen)
    _subscribers: list[typing.Callable[[], None]] = dataclasses.field(default_factory=list)
    _id: int = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        """
        Check whether the supplied event name is unique and not taken by another existing or internal event. If unique,
        add the event to the dictionary.

        :raises ValueError: All event names must be unique.
        """
        if self.name in _INTERNAL_EVENT_NAMES:
            raise ValueError(f'Cannot create event: {self.name}. An internal event of the same name already exists.')

        if self.name in EVENT_IDS:
            raise ValueError(f'Cannot create two events of the same name: {self.name}.')

        self._id = forge.core.utils.id.generate_random_id()

        _EVENTS[self._id] = self
        EVENT_IDS[self.name] = self._id

    def __iadd__(self, subscriber: typing.Callable[[], None]) -> Event:
        """
        Register a new function to the event using the '+=' operator.

        :param subscriber: Function to be registered to the event.
        :type subscriber: typing.Callable[[], None]

        :return: The event to which the function is registered.
        :rtype: Event

        :raises ValueError: All functions registered to the event must be unique.
        """
        if subscriber in self._subscribers:
            raise ValueError(f'Function {subscriber.__name__} is already subscribed to the event.')

        self._subscribers.append(subscriber)
        return self

    def __isub__(self, subscriber: typing.Callable[[], None]) -> Event:
        """
        Deregister an existing function to the event using the '-=' operator.

        :param subscriber: Function to be deregistered from the event.
        :type subscriber: typing.Callable[[], None]

        :return: THe event to which the function was registered.
        :rtype: Event

        :raises ValueError: A function that was never registered cannot be deregistered.
        """
        if subscriber not in self._subscribers:
            raise ValueError(f'Function {subscriber.__name__} never subscribed to the event.')

        self._subscribers.remove(subscriber)
        return self

    def __repr__(self) -> str:
        """
        Internal representation of the event.

        :return: Simple string with event name and subscriber count.
        :rtype: str
        """
        return f'Event -> Name: {self.name}, Subscriber Count: {len(self._subscribers)}'

    def __str__(self) -> str:
        """
        String representation of the event.

        :return: Detailed string with event information.
        :rtype: str
        """
        return f'Forge Event -> Name {self.name}, ID: {self._id}, Subscribers: {self._subscribers}'

    def id(self) -> int:
        """
        Get the unique ID of the event.

        :return: ID of the event.
        :rtype: int
        """
        return self._id

    def post(self) -> None:
        """
        Post the event that calls all of its subscriber functions. If an exception occurs when calling a subscriber
        function, it is logged as a warning instead.
        """
        for function in self._subscribers:
            try:
                function()

            except Exception as e:
                warnings.warn(f'Execution of {function.__name__} led to an exception.\n{e}')


def get_event_from_name(event_name: str) -> Event:
    """
    Retrieve a registered event from the event dictionary using the event name. Also does not allow the retrieval an
    internal event.

    :param event_name: Name of the event to be retrieved.
    :type event_name: str

    :return: Event stored in the event dictionary.
    :rtype: Event

    :raises ValueError: Internal events cannot be retrieved using their names.
    :raises KeyError: An event must be registered if it is to be retrieved.
    """
    if event_name in _INTERNAL_EVENT_NAMES:
        raise ValueError(f'Event named: {event_name} is an internal event and cannot be retrieved.')

    if event_name not in EVENT_IDS:
        raise KeyError(f'Event named: {event_name} has not been registered as an event and cannot be retrieved.')

    return _EVENTS[EVENT_IDS[event_name]]


def get_event_from_id(event_id: int) -> Event:
    """
    Retrieve a registered event from the event dictionary using the event ID. Allows the retrieval of an internal event.

    :param event_id: ID of the event to be retrieved.
    :type event_id: int

    :return: Event stored in the event dictionary.
    :rtype: Event

    :raises KeyError: An event must be registered if it is to be retrieved.
    """
    if event_id not in _EVENTS:
        raise KeyError(f'Event with ID: {event_id} has not been registered as an event and cannot be retrieved.')

    return _EVENTS[event_id]


def delete_event_from_name(event_name: str) -> None:
    """
    Delete a registered event from the event dictionary using the event name and free the ID of the event. Also does
    not allow the deletion of an internal event.

    :param event_name: Name of the event to be deleted.
    :type event_name: str

    :raises ValueError: Internal events cannot be deleted using their names.
    :raises KeyError: An event must be registered if it is to be deleted.
    """
    if event_name in _INTERNAL_EVENT_NAMES:
        raise ValueError(f'Event named: {event_name} is an internal event and cannot be deleted.')

    if event_name not in EVENT_IDS:
        raise KeyError(f'Event named: {event_name} has not been registered as an event and cannot be deleted.')

    _EVENTS.pop(EVENT_IDS[event_name])
    forge.core.utils.id.delete_id(EVENT_IDS[event_name])
    EVENT_IDS.pop(event_name)


def delete_event_from_id(event_id: int) -> None:
    """
    Delete a registered event from the event dictionary using the event ID and free the ID of the image. Allows the
    deletion of an internal event.

    :param event_id: ID of the event to be deleted.
    :type event_id: int

    :raises KeyError: An event must be registered if it to be deleted.
    """
    if event_id not in _EVENTS:
        raise KeyError(f'Event with ID: {event_id} has not been registered an an event and cannot be deleted.')

    event_name = _EVENTS.pop(event_id).name
    forge.core.utils.id.delete_id(event_id)
    EVENT_IDS.pop(event_name)
