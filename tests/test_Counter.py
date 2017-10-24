
from . import TestStdoutReader
import pyprogress


class TestCounter(TestStdoutReader):

    def tearDown(self):
        self.c.stop()
        self.c.join()
        TestStdoutReader.tearDown(self)

    def test_counter_no_total(self):
        output = ['0', '\b1', '\b2', '\b3', '\b4', '\b5']
        self.c = pyprogress.Counter()
        self.c.start()
        assert self.stdout.getvalue().strip() == output[0]
        self.stdout.truncate(0)
        for x in range(1, 6):
            self.c.inc()
            self.c.write()  # force write output
            assert self.stdout.getvalue().strip('\x00').strip() == output[x]
            self.stdout.truncate(0)

    def test_counter_with_total(self):
        output = ['0/5', '\b\b\b1/5', '\b\b\b2/5', '\b\b\b3/5', '\b\b\b4/5', '\b\b\b5/5']
        self.c = pyprogress.Counter(total=5)
        self.c.start()
        assert self.stdout.getvalue().strip() == output[0]
        self.stdout.truncate(0)
        for x in range(1, 6):
            self.c.inc()
            self.c.write()  # force write output
            assert self.stdout.getvalue().strip('\x00').strip() == output[x]
            self.stdout.truncate(0)

    def test_counter_initial(self):
        output = ['2', '\b3', '\b4', '\b5']
        self.c = pyprogress.Counter(initial=2)
        self.c.start()
        assert self.stdout.getvalue().strip() == output[0]
        self.stdout.truncate(0)
        for x in range(1, 4):
            self.c.inc()
            self.c.write()  # force write output
            assert self.stdout.getvalue().strip('\x00').strip() == output[x]
            self.stdout.truncate(0)

    def test_counter_inc_2(self):
        output = ['0/10',
                  '\b\b\b\b2/10',
                  '\b\b\b\b4/10',
                  '\b\b\b\b6/10',
                  '\b\b\b\b8/10',
                  '\b\b\b\b10/10']
        self.c = pyprogress.Counter(total=10)
        self.c.start()
        assert self.stdout.getvalue().strip() == output[0]
        self.stdout.truncate(0)
        for x in range(1, 6):
            self.c.inc(2)
            self.c.write()
            assert self.stdout.getvalue().strip('\x00').strip() == output[x]
            self.stdout.truncate(0)


class TestCounter(TestStdoutReader):

    def test_counter_no_total(self):
        output = ['0', '\b1', '\b2', '\b3', '\b4', '\b5']
        with pyprogress.Counter() as c:
            assert self.stdout.getvalue().strip() == output[0]
            self.stdout.truncate(0)
            for x in range(1, 6):
                c.inc()
                c.write()  # force write output
                assert self.stdout.getvalue().strip('\x00').strip() == output[x]
                self.stdout.truncate(0)

    def test_counter_with_total(self):
        output = ['0/5', '\b\b\b1/5', '\b\b\b2/5', '\b\b\b3/5', '\b\b\b4/5', '\b\b\b5/5']
        with pyprogress.Counter(total=5) as c:
            assert self.stdout.getvalue().strip() == output[0]
            self.stdout.truncate(0)
            for x in range(1, 6):
                c.inc()
                c.write()  # force write output
                assert self.stdout.getvalue().strip('\x00').strip() == output[x]
                self.stdout.truncate(0)

    def test_counter_initial(self):
        output = ['2', '\b3', '\b4', '\b5']
        with pyprogress.Counter(initial=2) as c:
            assert self.stdout.getvalue().strip() == output[0]
            self.stdout.truncate(0)
            for x in range(1, 4):
                c.inc()
                c.write()  # force write output
                assert self.stdout.getvalue().strip('\x00').strip() == output[x]
                self.stdout.truncate(0)

    def test_counter_inc_2(self):
        output = ['0/10',
                  '\b\b\b\b2/10',
                  '\b\b\b\b4/10',
                  '\b\b\b\b6/10',
                  '\b\b\b\b8/10',
                  '\b\b\b\b10/10']

        with pyprogress.Counter(total=10) as c:
            assert self.stdout.getvalue().strip() == output[0]
            self.stdout.truncate(0)
            for x in range(1, 6):
                c.inc(2)
                c.write()
                assert self.stdout.getvalue().strip('\x00').strip() == output[x]
                self.stdout.truncate(0)
