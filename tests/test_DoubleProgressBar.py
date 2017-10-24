from . import TestStdoutReader
import pyprogress
import re


class TestDoubleProgressBar(TestStdoutReader):

    def test_doubleprogressbar_expandpastlimitwithname(self):
        outputs = [
            'DoubleProgressBar \[ {40}\] 0\/2 \[ {20}\] 0\/5',
            '[\b]{73}\[ {40}\] 0\/2 \[#{8} {12}\] 2\/5',
            '[\b]{73}\[ {40}\] 0\/2 \[#{16} {4}\] 4\/5',
            '[\b]{73}\[ {40}\] 0\/2 \[#{20}\] 6\/5',
            '[\b]{73}\[ {40}\] 0\/2 \[#{20}\] 8\/5',
            '[\b]{73}\[ {40}\] 0\/2 \[#{20}\] 10\/5',
            '[\b]{74}\[#{20} {20}\] 1\/2 \[ {20}\] 0\/5',
            '[\b]{74}\[#{20} {20}\] 1\/2 \[#{8} {12}\] 2\/5',
            '[\b]{74}\[#{20} {20}\] 1\/2 \[#{16} {4}\] 4\/5',
            '[\b]{74}\[#{20} {20}\] 1\/2 \[#{20}\] 6\/5',
            '[\b]{74}\[#{20} {20}\] 1\/2 \[#{20}\] 8\/5',
            '[\b]{74}\[#{20} {20}\] 1\/2 \[#{20}\] 10\/5',
            '[\b]{74}\[#{40}\] 2\/2 \[ {20}\] 0\/5'
        ]
        i = 0
        self.p = pyprogress.DoubleProgressBar(2, 5, name="DoubleProgressBar")
        self.p.begin()
        assert re.match(outputs[i], self.stdout.getvalue().strip())
        i += 1
        self.stdout.truncate(0)

        for x in range(2):
            for y in range(5):
                self.p.inc2(2)
                assert re.match(outputs[i], self.stdout.getvalue().strip('\x00').strip())
                i += 1
                self.stdout.truncate(0)
            self.p.inc()
            self.stdout.truncate(0)
            self.p.reset2()
            assert re.match(outputs[i], self.stdout.getvalue().strip('\x00').strip())
            i += 1
            self.stdout.truncate(0)


class TestDoubleProgressBarInContext(TestStdoutReader):

    def test_doubleprogressbar_expandpastlimitwithname(self):
        outputs = [
            'DoubleProgressBar \[ {40}\] 0\/2 \[ {20}\] 0\/5',
            '[\b]{73}\[ {40}\] 0\/2 \[#{8} {12}\] 2\/5',
            '[\b]{73}\[ {40}\] 0\/2 \[#{16} {4}\] 4\/5',
            '[\b]{73}\[ {40}\] 0\/2 \[#{20}\] 6\/5',
            '[\b]{73}\[ {40}\] 0\/2 \[#{20}\] 8\/5',
            '[\b]{73}\[ {40}\] 0\/2 \[#{20}\] 10\/5',
            '[\b]{74}\[#{20} {20}\] 1\/2 \[ {20}\] 0\/5',
            '[\b]{74}\[#{20} {20}\] 1\/2 \[#{8} {12}\] 2\/5',
            '[\b]{74}\[#{20} {20}\] 1\/2 \[#{16} {4}\] 4\/5',
            '[\b]{74}\[#{20} {20}\] 1\/2 \[#{20}\] 6\/5',
            '[\b]{74}\[#{20} {20}\] 1\/2 \[#{20}\] 8\/5',
            '[\b]{74}\[#{20} {20}\] 1\/2 \[#{20}\] 10\/5',
            '[\b]{74}\[#{40}\] 2\/2 \[ {20}\] 0\/5'
        ]
        i = 0

        with pyprogress.DoubleProgressBar(2, 5, name="DoubleProgressBar") as p:
            assert re.match(outputs[i], self.stdout.getvalue().strip())
            i += 1
            self.stdout.truncate(0)

            for x in range(2):
                for y in range(5):
                    p.inc2(2)
                    assert re.match(outputs[i], self.stdout.getvalue().strip('\x00').strip())
                    i += 1
                    self.stdout.truncate(0)
                p.inc()
                self.stdout.truncate(0)
                p.reset2()
                assert re.match(outputs[i], self.stdout.getvalue().strip('\x00').strip())
                i += 1
                self.stdout.truncate(0)
