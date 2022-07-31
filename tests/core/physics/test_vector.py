import math
import random
from unittest import TestCase

import pygame

from core.physics import vector as vector


class TestVector2D(TestCase):
    rand_x: int = random.randint(-99, 99)
    rand_y: int = random.randint(-99, 99)

    def test_length(self):
        self.assertEqual(0, vector.Vector2D(0, 0).length())
        self.assertEqual(math.sqrt(2), vector.Vector2D(1, 1).length())
        self.assertEqual(math.sqrt(8), vector.Vector2D(-2, 2).length())

        self.assertEqual(
            pygame.math.Vector2(self.rand_x, self.rand_y).length(),
            vector.Vector2D(self.rand_x, self.rand_y).length()
        )

    def test_length_squared(self):
        self.assertEqual(0, vector.Vector2D(0, 0).length_squared())
        self.assertEqual(2, vector.Vector2D(1, 1).length_squared())
        self.assertEqual(8, vector.Vector2D(-2, 2).length_squared())

        self.assertEqual(
            pygame.math.Vector2(self.rand_x, self.rand_y).length_squared(),
            vector.Vector2D(self.rand_x, self.rand_y).length_squared()
        )

    def test_normalize(self):
        vec = vector.Vector2D(self.rand_x, self.rand_y)
        vec.normalize()

        # Account for certain floating-point inaccuracies.
        self.assertAlmostEqual(pygame.Vector2(self.rand_x, self.rand_y).normalize().length(), vec.length())

    def test_normalize_raises(self):
        zero_vec = vector.Vector2D(0, 0)
        self.assertRaises(ZeroDivisionError, zero_vec.normalize)

    def test_is_normalized(self):
        vec1 = vector.Vector2D(-1 / math.sqrt(2), 1 / math.sqrt(2))
        vec2 = vector.Vector2D(1, 2)

        # Account for certain floating-point inaccuracies.
        self.assertTrue(vec1.is_normalized())
        self.assertFalse(vec2.is_normalized())

    def test_as_tuple(self):
        vec = vector.Vector2D(self.rand_x, self.rand_y)
        self.assertEqual((self.rand_x, self.rand_y), vec.as_tuple())

    def test_vector_clamp(self):
        vec = vector.Vector2D(100, -100)
        min_ = vector.Vector2D(0, 0)
        max_ = vector.Vector2D(50, 100)
        clamped_vec: vector.Vector2D = vector.clamp(vec, min_, max_)

        self.assertTrue(min_.x <= clamped_vec.x <= max_.x and min_.y <= clamped_vec.y <= max_.y)

    def test_vector_clamp_raises(self):
        vec = vector.Vector2D(100, -100)
        min_ = vector.Vector2D(0, 0)
        max_ = vector.Vector2D(50, 100)

        self.assertRaises(ValueError, vector.clamp, vec, max_, min_)

    def test_vector_normalized(self):
        vec = vector.Vector2D(self.rand_x, self.rand_y)
        normal = vector.normalized(vec)

        # Account for certain floating-point inaccuracies.
        self.assertAlmostEqual(1, normal.length())

    def test_vector_normalized_raises(self):
        zero_vec = vector.Vector2D(0, 0)
        self.assertRaises(ZeroDivisionError, vector.normalized, zero_vec)

    def test_vector_angle(self):
        vec = vector.Vector2D(self.rand_x, self.rand_y)
        vec2 = vector.Vector2D(-2, 1)
        vec3 = vector.Vector2D(1, -2)

        self.assertEqual(0, vector.angle(vec, vec))
        self.assertEqual(2.498091544796509, vector.angle(vec2, vec3))

    def test_vector_lerp(self):
        from_vector = vector.Vector2D(2, 8)
        to_vector = vector.Vector2D(5, 8)

        self.assertEqual(from_vector, vector.lerp(from_vector, to_vector, 0))
        self.assertEqual(to_vector, vector.lerp(from_vector, to_vector, 1))
        self.assertEqual(vector.Vector2D(4.1, 8), vector.lerp(from_vector, to_vector, 0.7))

    def test_vector_distance_between(self):
        vec = vector.Vector2D(100, -10)
        vec2 = vector.Vector2D(1, -1)

        # Account for certain floating-point inaccuracies.
        self.assertAlmostEqual(99.40824915468535, vector.distance_between(vec, vec2))

    def test_vector_distance_squared_between(self):
        vec = vector.Vector2D(100, -10)
        vec2 = vector.Vector2D(1, -1)

        self.assertEqual(9882, vector.distance_squared_between(vec, vec2))

    def test_vector_reflect(self):
        direction = vector.Vector2D(1, 2)
        normal = vector.Vector2D(0, 1)

        self.assertEqual(vector.Vector2D(1, -2), vector.reflect(direction, normal))

    def test_vector_reflect_raises(self):
        direction = vector.Vector2D(self.rand_x, self.rand_y)
        normal = vector.Vector2D(100, -2)

        self.assertRaises(ValueError, vector.reflect, direction, normal)

    def test_vector_from_tuple(self):
        vec = vector.Vector2D(self.rand_x, self.rand_y)
        self.assertEqual(vec, vector.from_tuple((self.rand_x, self.rand_y)))
