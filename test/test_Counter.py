
import test
import pyprogress


class TestCounter(test.TestStdoutReader):

    def tearDown(self):
        self.c.stop()
        self.c.join()
        test.TestStdoutReader.tearDown(self)

    def test_counter_no_total(self):
        output = ['0', '\b1', '\b2', '\b3', '\b4', '\b5']
        self.c = pyprogress.Counter()
        self.c.start()
        assert self.stdout.getvalue().strip() == output[0]
        self.stdout.truncate(0)
        for x in range(1, 6):
            self.c.inc()
            self.c.write()  # force write output
            assert self.stdout.getvalue().strip() == output[x]
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
            assert self.stdout.getvalue().strip() == output[x]
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
            assert self.stdout.getvalue().strip() == output[x]
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
            assert self.stdout.getvalue().strip() == output[x]
            self.stdout.truncate(0)
