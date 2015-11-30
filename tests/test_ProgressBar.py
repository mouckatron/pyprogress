
from . import TestStdoutReader
import pyprogress
import re
from time import sleep


class TestProgressBar(TestStdoutReader):

    def tearDown(self):
        self.p.end()
        TestStdoutReader.tearDown(self)

    def test_progressbar_default(self):
        outputs = [
            '[                                        ] 0/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[####                                    ] 1/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########                                ] 2/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[############                            ] 3/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[################                        ] 4/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[####################                    ] 5/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################                ] 6/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[############################            ] 7/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[################################        ] 8/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[####################################    ] 9/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 10/10'
        ]
        self.p = pyprogress.ProgressBar(10)
        self.p.begin()
        assert self.stdout.getvalue().strip() == outputs[0]
        self.stdout.truncate(0)

        for x in range(1, 11):
            self.p.inc()
            assert self.stdout.getvalue().strip() == outputs[x]
            self.stdout.truncate(0)

    def test_progressbar_inc2(self):
        outputs = [
            '[                                        ] 0/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########                                ] 2/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[################                        ] 4/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################                ] 6/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[################################        ] 8/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 10/10'
        ]
        self.p = pyprogress.ProgressBar(10)
        self.p.begin()
        assert self.stdout.getvalue().strip() == outputs[0]
        self.stdout.truncate(0)
        for x in range(1, 6):
            self.p.inc(2)
            assert self.stdout.getvalue().strip() == outputs[x]
            self.stdout.truncate(0)

    def test_progressbar_expandpastlimit(self):
        outputs = [
            '[                                        ] 0/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########                                ] 2/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[################                        ] 4/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################                ] 6/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[################################        ] 8/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 10/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 12/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 14/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 16/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 18/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 20/10'
        ]
        self.p = pyprogress.ProgressBar(10)
        self.p.begin()
        assert self.stdout.getvalue().strip() == outputs[0]
        self.stdout.truncate(0)
        for x in range(1, 11):
            self.p.inc(2)
            if self.stdout.getvalue().strip() != outputs[x]:
                print >> sys.stderr, "\n"
                print >> sys.stderr, repr(outputs[x])
                print >> sys.stderr, repr(self.stdout.getvalue().strip())
            assert self.stdout.getvalue().strip() == outputs[x]
            self.stdout.truncate(0)

    def test_progressbar_withname(self):
        outputs = [
            'ProgressBar [                                        ] 0/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[####                                    ] 1/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########                                ] 2/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[############                            ] 3/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[################                        ] 4/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[####################                    ] 5/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################                ] 6/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[############################            ] 7/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[################################        ] 8/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[####################################    ] 9/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 10/10'
        ]
        self.p = pyprogress.ProgressBar(10, name="ProgressBar")
        self.p.begin()
        assert self.stdout.getvalue().strip() == outputs[0]
        self.stdout.truncate(0)
        for x in range(1, 11):
            self.p.inc()
            assert self.stdout.getvalue().strip() == outputs[x]
            self.stdout.truncate(0)

    def test_progressbar_expandpastlimitwithname(self):
        outputs = [
            'ProgressBar [                                        ] 0/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########                                ] 2/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[################                        ] 4/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################                ] 6/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[################################        ] 8/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 10/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 12/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 14/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 16/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 18/10',
            '\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b[########################################] 20/10'
        ]
        self.p = pyprogress.ProgressBar(10, name="ProgressBar")
        self.p.begin()
        assert self.stdout.getvalue().strip() == outputs[0]
        self.stdout.truncate(0)
        for x in range(1, 11):
            self.p.inc(2)
            assert self.stdout.getvalue().strip() == outputs[x]
            self.stdout.truncate(0)

    def test_progressbar_withruntime(self):
        outputs = [
            '0:00:00\.[0-9]{6} \[ {40}\] 0\/5 [0-9.]+\/s',
            '[\b]{65}0:00:01\.[0-9]{6} \[#{8} {32}\] 1\/5 [0-9.]+\/s',
            '[\b]{69}0:00:02\.[0-9]{6} \[#{16} {24}\] 2\/5 [0-9.]+\/s',  # \b length increases as items per second displays 1.000 instead of 0 because of zero division error
            '[\b]{69}0:00:03\.[0-9]{6} \[#{24} {16}\] 3\/5 [0-9.]+\/s',
            '[\b]{69}0:00:04\.[0-9]{6} \[#{32} {8}\] 4\/5 [0-9.]+\/s',
            '[\b]{69}0:00:05\.[0-9]{6} \[#{40}\] 5\/5 [0-9.]+\/s'
        ]
        self.p = pyprogress.ProgressBar(5, timecount=True)
        self.p.begin()
        assert re.match(outputs[0], self.stdout.getvalue().strip())
        self.stdout.truncate(0)
        sleep(1)
        for x in range(1, 6):
            self.p.inc(1)
            assert re.match(outputs[x], self.stdout.getvalue().strip())
            self.stdout.truncate(0)
            sleep(1)

    def test_progressbar_completionprediction(self):
        outputs = [
            '\[ {40}\] 0\/5 0\/s',
            '[\b]{51}4\.[0-9]{3} \[#{8} {32}\] 1\/5 [0-9.]+\/s',
            '[\b]{60}3\.[0-9]{3} \[#{16} {24}\] 2\/5 [0-9.]+\/s',  # \b length increases as items per second displays 1.000 instead of 0 because of zero division error and completionprediction shows
            '[\b]{60}2\.[0-9]{3} \[#{24} {16}\] 3\/5 [0-9.]+\/s',
            '[\b]{60}1\.[0-9]{3} \[#{32} {8}\] 4\/5 [0-9.]+\/s',
            '[\b]{60}0\.[0-9]{3} \[#{40}\] 5\/5 [0-9.]+\/s'
        ]
        self.p = pyprogress.ProgressBar(5, completionprediction=True)
        self.p.begin()
        assert re.match(outputs[0], self.stdout.getvalue().strip())
        self.stdout.truncate(0)
        sleep(1)
        for x in range(1, 6):
            self.p.inc(1)
            assert re.match(outputs[x], self.stdout.getvalue().strip())
            self.stdout.truncate(0)
            sleep(1)

    def test_progressbar_changeprogresschar(self):
        outputs = [
            '\[                                        \] 0\/10',
            '\b{47}\[----                                    \] 1\/10',
            '\b{47}\[--------                                \] 2\/10',
            '\b{47}\[------------                            \] 3\/10',
            '\b{47}\[----------------                        \] 4\/10',
            '\b{47}\[--------------------                    \] 5\/10',
            '\b{47}\[------------------------                \] 6\/10',
            '\b{47}\[----------------------------            \] 7\/10',
            '\b{47}\[--------------------------------        \] 8\/10',
            '\b{47}\[------------------------------------    \] 9\/10',
            '\b{47}\[----------------------------------------\] 10\/10'
        ]
        self.p = pyprogress.ProgressBar(10, progresschar='-')
        self.p.begin()
        assert re.match(outputs[0], self.stdout.getvalue().strip())
        self.stdout.truncate(0)
        for x in range(1, 11):
            self.p.inc(1)
            assert re.match(outputs[x], self.stdout.getvalue().strip())
            self.stdout.truncate(0)

    def test_progressbar_changewidth(self):
        outputs = [
            '\[ {80}\] 0\/8',
            '\b{86}\[#{10} {70}\] 1\/8',
            '\b{86}\[#{20} {60}\] 2\/8',
            '\b{86}\[#{30} {50}\] 3\/8',
            '\b{86}\[#{40} {40}\] 4\/8',
            '\b{86}\[#{50} {30}\] 5\/8',
            '\b{86}\[#{60} {20}\] 6\/8',
            '\b{86}\[#{70} {10}\] 7\/8',
            '\b{86}\[#{80}\] 8\/8',
        ]
        self.p = pyprogress.ProgressBar(8, width=80)
        self.p.begin()
        assert re.match(outputs[0], self.stdout.getvalue().strip())
        self.stdout.truncate(0)
        for x in range(1, 9):
            self.p.inc(1)
            assert re.match(outputs[x], self.stdout.getvalue().strip())
            self.stdout.truncate(0)

    def test_progressbar_coloredips(self):
        outputs = [
            '0:00:00\.[0-9]{6} \[ {40}\] 0\/5 0\/s',
            '[\b]{56}0:00:01\.[0-9]{6} \[#{8} {32}\] 1\/5 \x1b\[92m[0-9.]+\x1b\[0m\/s',
            '[\b]{69}0:00:02\.[0-9]{6} \[#{16} {24}\] 2\/5 \x1b\[92m[0-9.]+\x1b\[0m\/s',
            '[\b]{69}0:00:03\.[0-9]{6} \[#{24} {16}\] 3\/5 \x1b\[92m[0-9.]+\x1b\[0m\/s',
            '[\b]{69}0:00:04\.[0-9]{6} \[#{32} {8}\] 4\/5 \x1b\[92m[0-9.]+\x1b\[0m\/s',
            '[\b]{69}0:00:05\.[0-9]{6} \[#{40}\] 5\/5 \x1b\[92m[0-9.]+\x1b\[0m\/s'
        ]
        self.p = pyprogress.ProgressBar(5, colored=True, timecount=True)
        self.p.begin()
        assert re.match(outputs[0], self.stdout.getvalue().strip())
        self.stdout.truncate(0)
        sleep(1)
        for x in range(1, 6):
            self.p.inc(1)
            assert re.match(outputs[x], self.stdout.getvalue().strip())
            self.stdout.truncate(0)
            sleep(1)

    def test_progressbar_everything(self):
        outputs = [
            'ProgressBar 0:00:00\.[0-9]{6}  \[ {100}\] 0\/20 0\/s',
            '[\b]{118}0:00:00\.[0-9]{6} [0-9.]{5} \[#{5} {95}\] 1\/20 0\/s',
            '[\b]{123}0:00:01\.[0-9]{6} [0-9.]{5} \[#{10} {90}\] 2\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{136}0:00:01\.[0-9]{6} [0-9.]{5} \[#{15} {85}\] 3\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{136}0:00:02\.[0-9]{6} [0-9.]{5} \[#{20} {80}\] 4\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{136}0:00:02\.[0-9]{6} [0-9.]{5} \[#{25} {75}\] 5\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{136}0:00:03\.[0-9]{6} [0-9.]{5} \[#{30} {70}\] 6\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{136}0:00:03\.[0-9]{6} [0-9.]{5} \[#{35} {65}\] 7\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{136}0:00:04\.[0-9]{6} [0-9.]{5} \[#{40} {60}\] 8\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{136}0:00:04\.[0-9]{6} [0-9.]{5} \[#{45} {55}\] 9\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{136}0:00:05\.[0-9]{6} [0-9.]{5} \[#{50} {50}\] 10\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{137}0:00:05\.[0-9]{6} [0-9.]{5} \[#{55} {45}\] 11\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{137}0:00:06\.[0-9]{6} [0-9.]{5} \[#{60} {40}\] 12\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{137}0:00:06\.[0-9]{6} [0-9.]{5} \[#{65} {35}\] 13\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{137}0:00:07\.[0-9]{6} [0-9.]{5} \[#{70} {30}\] 14\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{137}0:00:07\.[0-9]{6} [0-9.]{5} \[#{75} {25}\] 15\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{137}0:00:08\.[0-9]{6} [0-9.]{5} \[#{80} {20}\] 16\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{137}0:00:08\.[0-9]{6} [0-9.]{5} \[#{85} {15}\] 17\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{137}0:00:09\.[0-9]{6} [0-9.]{5} \[#{90} {10}\] 18\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{137}0:00:09\.[0-9]{6} [0-9.]{5} \[#{95} {5}\] 19\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s',
            '[\b]{137}0:00:10\.[0-9]{6} [0-9.]{5} \[#{100}\] 20\/20 \x1b\[9[12]m[0-9.]+\x1b\[0m\/s'
        ]
        self.p = pyprogress.ProgressBar(20, width=100, name="ProgressBar", timecount=True, completionprediction=True, colored=True)
        self.p.begin()
        assert re.match(outputs[0], self.stdout.getvalue().strip())
        self.stdout.truncate(0)
        sleep(0.5)
        for x in range(1, 21):
            self.p.inc(1)
            assert re.match(outputs[x], self.stdout.getvalue().strip())
            self.stdout.truncate(0)
            sleep(0.5)
