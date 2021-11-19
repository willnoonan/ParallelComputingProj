import unittest
from testingtools import blurimageby
from imagetools import *

class MyTestCase(unittest.TestCase):
    def test_algorithms_equal(self):
        v1 = blurimageby(simple_boxblur)["red"].result()
        v2 = blurimageby(simple_boxblur_V2)["red"].result()
        self.assertEqual(v1, v2)  # add assertion here


if __name__ == '__main__':
    unittest.main()
