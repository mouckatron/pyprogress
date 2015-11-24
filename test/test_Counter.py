
import unittest
import pyprogress
from time import sleep


class TestCounter(unittest.TestCase):

    def tearDown(self):
        self.c.stop()
        self.c.join()

    def test_counter_no_total(self):
        self.c = pyprogress.Counter()
        self.c.start()
        for x in range(5):
            self.c.inc()
            sleep(0.5)

    def test_counter_with_total(self):
        self.c = pyprogress.Counter(total=5)
        self.c.start()
        for x in range(5):
            self.c.inc()
            sleep(0.5)

    def test_counter_initial(self):
        self.c = pyprogress.Counter(initial=2)
        self.c.start()
        for x in range(5):
            self.c.inc()
            sleep(0.5)

    def test_counter_inc_2(self):
        self.c = pyprogress.Counter(total=10)
        self.c.start()
        for x in range(5):
            self.c.inc(2)
            sleep(0.5)


if __name__ == '__main__':
    unittest.main()
