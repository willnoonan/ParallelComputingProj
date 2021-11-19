import unittest
from testingtools import blurimageby
from imagetools import *

class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Put variables in setUpClass that you want executed only once and available to all tests.
        """
        cls.v1 = blurimageby(simple_boxblur)["red"].result()

    def test_algorithms_equal(self):
        v2 = blurimageby(boxblur, radius=1)["red"].result()
        self.assertEqual(self.v1, v2)  # add assertion here

    def test_algorithms_notequal(self):
        v2 = blurimageby(boxblur, radius=2)["red"].result()
        self.assertNotEqual(self.v1, v2)

if __name__ == '__main__':
    unittest.main()
