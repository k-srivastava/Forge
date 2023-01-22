"""
Creation, retrieval, posting and deletion of events using Forge's custom event management system.
"""
import dataclasses
import enum
import typing
import warnings

import attrs

import forge.core.utils.exceptions
import forge.core.utils.id

_EVENTS: dict[int, 'Event'] = {}
EVENT_NAMES: dict[str, int] = {}
INTERNAL_EVENT_NAMES: list[str] = []


class InternalEvent(enum.Enum):
    """
    Enumeration of all internal events used by Forge.
    """
    MOUSE_CLICKED = '<MOUSE-CLICKED>'
    MOUSE_DEPRESSED = '<MOUSE-DEPRESSED>'
    KEY_PRESSED = '<KEY-PRESSED>'


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

        :raises forge.core.utils.exceptions.EventNameError: All event names must be unique.
        """
        if self.name in INTERNAL_EVENT_NAMES:
            raise forge.core.utils.exceptions.EventNameError(
                f'Cannot use event name: {self.name}. An internal event of the same name already exists.'
            )

        if self.name in EVENT_NAMES:
            raise forge.core.utils.exceptions.EventNameError(
                f'Cannot use event name: {self.name}. An event of the same name already exists.'
            )

        self._id = forge.core.utils.id.generate_random_id()

        _EVENTS[self._id] = self
        EVENT_NAMES[self.name] = self._id

    def __iadd__(self, subscriber: typing.Callable[[], None]) -> typing.Self:
        """
        Register a new function to the event using the '+=' operator.

        :param subscriber: Function to be registered to the event.
        :type subscriber: typing.Callable[[], None]

        :return: The event to which the function is registered.
        :rtype: Event

        :raises ValueError: All functions registered to the event must be unique.
        """
        if subscriber in self._subscribers:
            warnings.warn(f'Function {subscriber.__name__} is already subscribed to the event: {self.name}.')
            return self

        self._subscribers.append(subscriber)
        return self

    def __isub__(self, subscriber: typing.Callable[[], None]) -> typing.Self:
        """
        Deregister an existing function to the event using the '-=' operator.

        :param subscriber: Function to be deregistered from the event.
        :type subscriber: typing.Callable[[], None]

        :return: THe event to which the function was registered.
        :rtype: Event

        :raises ValueError: A function that was never registered cannot be deregistered.
        """
        if subscriber not in self._subscribers:
            warnings.warn(f'Function {subscriber.__name__} never subscribed to the event: {self.name}.')
            return self

        self._subscribers.remove(subscriber)
        return self

    def __repr__(self) -> str:
        """
        Internal representation of the event.

        :return: Simple string with event data.
        :rtype: str
        """
        return f'Event -> Name: {self.name}, Subscriber Count: {len(self._subscribers)}'

    def __str__(self) -> str:
        """
        String representation of the event.

        :return: Detailed string with event data.
        :rtype: str
        """
        return f'Forge Event -> Name {self.name}, Subscribers: {self._subscribers}'

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


def get_internal_event(event: InternalEvent) -> Event:
    """
    Retrieve a registered internal event from the event dictionary using the event enum.

    :param event: Enum name of the internal event to be retrieved.
    :type event: InternalEvent

    :return: Internal event stored in the event dictionary.
    :rtype: Event

    :raises forge.core.utils.exceptions.EventNotRegisteredError: An internal event must be registered if it is to be
                                                                 retrieved.
    """
    # The corresponding value for the enum will always be a string.
    # noinspection PyTypeHints
    event.value: str

    if event.value not in INTERNAL_EVENT_NAMES:
        raise forge.core.utils.exceptions.EventNotRegisteredError(
            f'Event named: {event.value} has not been registered as an internal event and cannot retrieved.'
        )

    return _EVENTS[EVENT_NAMES[event.value]]


def get_event_from_name(event_name: str) -> Event:
    """
    Retrieve a registered event from the event dictionary using the event name. Also does not allow the retrieval an
    internal event.

    :param event_name: Name of the event to be retrieved.
    :type event_name: str

    :return: Event stored in the event dictionary.
    :rtype: Event

    :raises forge.core.utils.exceptions.InternalEventRetrievalError: Internal events cannot be retrieved by using names.
    :raises forge.core.utils.exceptions.EventNotRegisteredError: An event must be registered if it is to be retrieved.
    """
    if event_name in INTERNAL_EVENT_NAMES:
        raise forge.core.utils.exceptions.InternalEventRetrievalError(event_name)

    if event_name not in EVENT_NAMES:
        raise forge.core.utils.exceptions.EventNotRegisteredError(
            f'Event named: {event_name} has not been registered as an event and cannot be retrieved.'
        )

    return _EVENTS[EVENT_NAMES[event_name]]


def get_event_from_id(event_id: int) -> Event:
    """
    Retrieve a registered event from the event dictionary using the event ID.

    :param event_id: ID of the event to be retrieved.
    :type event_id: int

    :return: Event stored in the event dictionary.
    :rtype: Event

    :raises forge.core.utils.exceptions.EventNotRegisteredError: An event must be registered if it is to be retrieved.
    """
    if event_id not in _EVENTS:
        raise forge.core.utils.exceptions.EventNotRegisteredError(
            f'Event with ID: {event_id} has not been registered as an event and cannot be retrieved.'
        )

    return _EVENTS[event_id]


def delete_event_from_name(event_name: str) -> None:
    """
    Delete a registered event from the event dictionary using the event name and free the ID of the event. Also does
    not allow the deletion of an internal event.

    :param event_name: Name of the event to be deleted.
    :type event_name: str

    :raises forge.core.utils.exceptions.IInternalEventDeletionError: Internal events cannot be deleted by using names.
    :raises forge.core.utils.exceptions.EventNotRegisteredError: An event must be registered if it is to be deleted.
    """
    if event_name in INTERNAL_EVENT_NAMES:
        raise forge.core.utils.exceptions.InternalEventDeletionError(event_name)

    if event_name not in EVENT_NAMES:
        raise forge.core.utils.exceptions.EventNotRegisteredError(
            f'Event named: {event_name} has not been registered as an event and cannot be deleted.'
        )

    _EVENTS.pop(EVENT_NAMES[event_name])
    forge.core.utils.id.delete_id(EVENT_NAMES[event_name])
    EVENT_NAMES.pop(event_name)


def delete_event_from_id(event_id: int) -> None:
    """
    Delete a registered event from the event dictionary using the event ID and free the ID of the image. Allows the
    deletion of an internal event.

    :param event_id: ID of the event to be deleted.
    :type event_id: int

    :raises forge.core.utils.exceptions.EventNotRegisteredError: An event must be registered if it to be deleted.
    """
    if event_id not in _EVENTS:
        raise forge.core.utils.exceptions.EventNotRegisteredError(
            f'Event with ID: {event_id} has not been registered an an event and cannot be deleted.'
        )

    event_name = _EVENTS.pop(event_id).name
    forge.core.utils.id.delete_id(event_id)
    EVENT_NAMES.pop(event_name)
