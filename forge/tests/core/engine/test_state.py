from unittest import TestCase

from forge.core.engine.state import create_state_variable


class TestState(TestCase):
    @staticmethod
    def create_variable():
        return create_state_variable(False)

    def test_getter(self):
        variable = 5
        getter, setter = create_state_variable(variable)

        self.assertEqual(variable, getter())

    def test_setter(self):
        string, set_string = create_state_variable('string')
        set_string('new string')

        self.assertEqual('new string', string())

    def test_modification(self):
        num, set_num = create_state_variable(0)

        for _ in range(10):
            set_num(num() + 1)

        self.assertEqual(10, num())

    def test_storage(self):
        boolean, set_boolean = self.create_variable()
        self.assertEqual(False, boolean())
