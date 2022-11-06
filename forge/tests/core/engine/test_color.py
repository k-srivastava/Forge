from unittest import TestCase

import pygame.color

from forge.core.engine.color import Color
from forge.core.utils.exceptions import RGBAColorError


class TestColor(TestCase):
    def test_initialization(self):
        self.assertRaises(RGBAColorError, Color, 300, 200, 200)
        self.assertRaises(RGBAColorError, Color, 80, 90, -20, 20.4)

    def test_as_tuple(self):
        color = Color(120, 80, 20, 65)

        self.assertEqual((120, 80, 20), color.as_tuple())
        self.assertEqual((120, 80, 20, 65), color.as_tuple(with_alpha=True))

    def test_as_pygame_color(self):
        forge_color = Color(80, 97, 20)
        pygame_color = pygame.color.Color(80, 97, 20)

        self.assertEqual(pygame_color, forge_color.as_pygame_color())
