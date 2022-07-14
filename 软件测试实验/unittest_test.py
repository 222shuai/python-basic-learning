import unittest


def add(a, b):
    return a + b


class TestAdd(unittest.TestCase):
    def test_add(self):
        a, b = 1, 2
        result = add(a, b)
        self.assertEqual(result, 4)


if __name__ == '__main__':
    unittest.main()
