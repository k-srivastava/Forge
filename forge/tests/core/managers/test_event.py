from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from forge.core.managers.event import Event
from forge.core.managers.event import delete_event_from_id, delete_event_from_name
from forge.core.managers.event import get_event_from_id, get_event_from_name


class TestEvent(TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def assertStdout(self, event: Event, expected_output: str, mock_output: StringIO):
        event.post()
        self.assertEqual(expected_output, mock_output.getvalue())

    def test_post_init_with_existing_name(self):
        event = Event('<test-post-init-enemy-hit>')
        self.assertRaises(ValueError, Event, '<test-post-init-enemy-hit>')

    def test_post(self):
        event = Event('<test-post-enemy-hit>')

        def enemy_status(name: str) -> None:
            print(f'You hit {name} for 10 HP of damage.')

        def announce_hit() -> None:
            print('ENEMY HIT!')

        def reload_gun() -> None:
            print('Reloading!')

        event += enemy_status, ('alien',)
        event += announce_hit, (),
        event += reload_gun, (),

        self.assertStdout(event, 'You hit alien for 10 HP of damage.\nENEMY HIT!\nReloading!\n')

        event -= announce_hit

        self.assertStdout(event, 'You hit alien for 10 HP of damage.\nReloading!\n')

    def test_get_event_from_name(self):
        event1 = Event('<event-name-1>')
        event2 = Event('<event-name-2>')

        self.assertEqual(event1, get_event_from_name('<event-name-1>'))

    def test_get_event_from_name_raises(self):
        self.assertRaises(KeyError, get_event_from_name, '<non-existent-event>')

    def test_get_event_from_id(self):
        event1 = Event('<event-id-1>')
        event1_id = event1.id()
        event2 = Event('<event-id-2>')

        self.assertEqual(event1, get_event_from_id(event1_id))

    def test_get_event_from_id_raises(self):
        self.assertRaises(KeyError, get_event_from_id, 0)

    def test_delete_event_from_name(self):
        event = Event('<deletion-name-event>')
        delete_event_from_name('<deletion-name-event>')

        # Deleting the event should remove it from the event dictionary causing a KeyError to be raised.
        self.assertRaises(KeyError, get_event_from_name, '<deletion-name-event>')

    def test_delete_event_from_name_raises(self):
        self.assertRaises(KeyError, delete_event_from_name, '<non-existent-event>')

    def test_delete_event_from_id(self):
        event = Event('<deletion-id-event>')
        event_id = event.id()
        delete_event_from_id(event_id)

        # Deleting the event should remove it from the event dictionary causing a KeyError to be raised.
        self.assertRaises(KeyError, get_event_from_id, event_id)

    def test_delete_event_from_id_raises(self):
        self.assertRaises(KeyError, delete_event_from_id, 0)
