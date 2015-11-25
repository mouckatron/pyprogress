
import test
import pyprogress
from time import sleep


class TestSpinner(test.TestStdoutReader):

    def test_spinner(self):
        output = ['|', '\b', '/', '\b', '-', '\b', '\\', '\b', '|', '\b', '/', '\b', '-', '\b']
        s = pyprogress.Spinner()
        s.start()
        sleep(2)
        s.stop()
        s.join()
        assert self.stdout.getvalue().strip() == ''.join(output[:len(self.stdout.getvalue().strip())])
