import unittest

from wrap import wrap_text


class WrapTest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(wrap_text("Hello!", 80), ["Hello!"])
        self.assertEqual(wrap_text("", 80), [""])


if __name__ == "__main__":
    unittest.main()
