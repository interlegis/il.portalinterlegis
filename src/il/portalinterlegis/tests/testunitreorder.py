# -*- coding: utf-8 -*-
import unittest2 as unittest

# TODO: mover isso para o lugar certo se realmente for usar... senão apagar
class NiceList(list):
    """A list with helper methods for moving an item up and down
    in a circular way, and inserting also after another item
    """

    @property
    def lastindex(self):
        return len(self) - 1

    def _swap(self, i, j):
        self[i], self[j] = self[j], self[i]

    def up(self, index):
        if index == 0:
            self.append(self.pop(0))
        else:
            self._swap(index - 1, index)

    def down(self, index):
        if index == self.lastindex:
            self.insert(0, self.pop())
        else:
            self._swap(index, (index + 1) % len(self))

    def insert_after(self, index, obj):
        self.insert(index + 1, obj)

_ = 999

class TestNiceList(unittest.TestCase):

    def test_up(self):
        a = NiceList([0, _, 1])
        a.up(a.index(_))
        self.assertEqual(a, [_, 0, 1])
        a.up(a.index(_))
        self.assertEqual(a, [0, 1, _])
        a.up(a.index(_))
        self.assertEqual(a, [0, _, 1])

    def test_down(self):
        a = NiceList([0, _, 1])
        a.down(a.index(_))
        self.assertEqual(a, [0, 1, _])
        a.down(a.index(_))
        self.assertEqual(a, [_, 0, 1])
        a.down(a.index(_))
        self.assertEqual(a, [0, _, 1])

    def test_insert_after(self):
        a = NiceList([0, 1])
        a.insert_after(1, _)
        self.assertEqual(a, [0, 1, _])

        a = NiceList([0, 1])
        a.insert_after(10, _)
        self.assertEqual(a, [0, 1, _])

