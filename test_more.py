from unittest import TestCase
from traceback import format_exc
from more import take, chunked, first


class TakeTest(TestCase):
    def test_simple_take(self):
        self.assertEqual(take(range(10), 5), [0, 1, 2, 3, 4])

    def test_null_take(self):
        self.assertEqual(take(range(10), 0), [])

    def test_negative_take(self):
        self.assertRaises(ValueError, lambda: take(-3, range(10)))

    def test_take_too_much(self):
        self.assertEqual(take(range(5), 10), [0, 1, 2, 3, 4])


class ChunkedTest(TestCase):
    def test_even(self):
        self.assertEqual(
           list(chunked('ABCDEF', 3)), [['A', 'B', 'C'], ['D', 'E', 'F']]
        )

    def test_odd(self):
        self.assertEqual(
            list(chunked('ABCDE', 3)), [['A', 'B', 'C'], ['D', 'E']]
        )

    def test_none(self):
        self.assertEqual(
            list(chunked('ABCDEF', None)), [['A', 'B', 'C', 'D', 'E', 'F']]
        )

    def test_strict_false(self):
        self.assertEqual(
            list(chunked('ABCDEF', 3, strict=False)), [['A', 'B', 'C'], ['D', 'E', 'F']]
        )

    def test_strict_true(self):
        def func_chunked():
            return list(chunked('ABCDE', 3, strict=True))

        self.assertRaisesRegex(ValueError, 'iterator is ont divisible by n', func_chunked)
        self.assertEqual(list(chunked('ABCDEF', 3, strict=True)), [['A', 'B', 'C'], ['D', 'E', 'F']])

    def test_strict_true_size_none(self):
        def func_chunked():
            return list(chunked('ABCDEF', None, strict=True))

        self.assertRaisesRegex(ValueError, '`n` cant be None when strict is True', func_chunked)


class FirstTest(TestCase):
    def test_many(self):
        self.assertEqual(first(x for x in range(4)), 0)

    def test_one(self):
        self.assertEqual(first([3]), 3)

    def test_default(self):
        self.assertEqual(first([], 'ook'), 'ook')

    def test_empty_stop_iteration(self):
        try:
            first([])
        except ValueError:
            format_exec = format_exc()
            self.assertIn("StopIteration", format_exec)
            self.assertIn("The above exception was the direct cause", format_exec)
        else:
            self.fail()
