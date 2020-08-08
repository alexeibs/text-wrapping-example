import unittest

from wrap import wrap_text


class WrapTest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(wrap_text('Hello!', 80), ['Hello!'])
        self.assertEqual(wrap_text('', 80), [''])

    def test_width_constraints(self):
        self.check_text('one', 10)
        self.check_text('one two three', 10)
        self.check_text('bigword and small', 5)

    def check_text(self, original_text, column_width):
        wrapped_text = wrap_text(original_text, column_width)
        for line in wrapped_text:
            self.assertLessEqual(len(line), column_width)
        original_chars = original_text.replace(' ', '')
        wrapped_chars = ''.join(wrapped_text).replace(' ', '')
        self.assertEqual(original_chars, wrapped_chars)


if __name__ == "__main__":
    unittest.main()
