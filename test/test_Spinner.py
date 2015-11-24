
import unittest
import pyprogress
from time import sleep


class TestSpinner(unittest.TestCase):

    def test_spinner(self):
        s = pyprogress.Spinner()
        s.start()
        sleep(2)
        s.stop()

if __name__ == '__main__':
    unittest.main()
