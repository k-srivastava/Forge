from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from core.events.event import Event
from core.events.event import get_event, delete_event


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

    def test_get_event(self):
        event1 = Event('<event-1>')
        event2 = Event('<event-2>')

        self.assertEqual(event1, get_event('<event-1>'))

    def test_get_event_raises(self):
        self.assertRaises(KeyError, get_event, '<non-existent-event>')

    def test_delete_event(self):
        event = Event('<deletion-event>')
        delete_event('<deletion-event>')

        # Deleting the event should remove it from the event dictionary causing a KeyError to be raised.
        self.assertRaises(KeyError, get_event, '<deletion-event>')

    def test_delete_event_raises(self):
        self.assertRaises(KeyError, delete_event, '<non-existent-event>')
