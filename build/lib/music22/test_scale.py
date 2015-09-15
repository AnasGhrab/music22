import unittest
import scale2

class ScaleTest(unittest.TestScale):
    """Tests for `scale2.py`."""

    def test_the_argument_type(self):
        """Is the argument for scale a list of float?"""
        self.assertTrue(is_prime(5))

if __name__ == '__main__':
    unittest.main()