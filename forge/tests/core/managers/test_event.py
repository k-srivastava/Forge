from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from forge.core.managers.event import Event
from forge.core.managers.event import delete_event_from_id, delete_event_from_name
from forge.core.managers.event import get_event_from_id, get_event_from_name
from forge.core.utils.exceptions import EventNameError, EventNotRegisteredError


class TestEvent(TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def assertStdout(self, event: Event, expected_output: str, mock_output: StringIO):
        event.post()
        self.assertEqual(expected_output, mock_output.getvalue())

    def test_post_init_with_existing_name(self):
        event = Event('<TEST-POST-INIT-ENEMY-HIT>')
        self.assertRaises(EventNameError, Event, '<TEST-POST-INIT-ENEMY-HIT>')

    def test_post(self):
        event = Event('<TEST-POST-ENEMY-HIT>')

        def enemy_status(name: str) -> None:
            print(f'You hit {name} for 10 HP of damage.')

        def announce_hit() -> None:
            print('Enemy hit!')

        def reload_gun() -> None:
            print('Reloading!')

        event += lambda: enemy_status('alien')
        event += announce_hit
        event += reload_gun

        self.assertStdout(event, 'You hit alien for 10 HP of damage.\nEnemy hit!\nReloading!\n')

        event -= announce_hit

        self.assertStdout(event, 'You hit alien for 10 HP of damage.\nReloading!\n')

    def test_get_event_from_name(self):
        event1 = Event('<EVENT-NAME-1>')
        event2 = Event('<EVENT-NAME-2>')

        self.assertEqual(event1, get_event_from_name('<EVENT-NAME-1>'))

    def test_get_event_from_name_raises(self):
        self.assertRaises(EventNotRegisteredError, get_event_from_name, '<NON-EXISTENT-EVENT>')

    def test_get_event_from_id(self):
        event1 = Event('<EVENT-ID-1>')
        event2 = Event('<EVENT-ID-2>')

        event1_id = event1.id()

        self.assertEqual(event1, get_event_from_id(event1_id))

    def test_get_event_from_id_raises(self):
        self.assertRaises(EventNotRegisteredError, get_event_from_id, 0)

    def test_delete_event_from_name(self):
        event = Event('<DELETION-NAME-EVENT>')
        delete_event_from_name('<DELETION-NAME-EVENT>')

        # Deleting the event should remove it from the event dictionary causing an EventNotRegisteredError to be raised.
        self.assertRaises(EventNotRegisteredError, get_event_from_name, '<DELETION-NAME-EVENT>')

    def test_delete_event_from_name_raises(self):
        self.assertRaises(EventNotRegisteredError, delete_event_from_name, '<NON-EXISTENT-EVENT>')

    def test_delete_event_from_id(self):
        event = Event('<DELETION-ID-EVENT>')
        event_id = event.id()
        delete_event_from_id(event_id)

        # Deleting the event should remove it from the event dictionary causing an EventNotRegisteredError to be raised.
        self.assertRaises(EventNotRegisteredError, get_event_from_id, event_id)

    def test_delete_event_from_id_raises(self):
        self.assertRaises(EventNotRegisteredError, delete_event_from_id, 0)
