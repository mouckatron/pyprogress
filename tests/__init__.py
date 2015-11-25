
import unittest
from StringIO import StringIO
import sys


class TestStdoutReader(unittest.TestCase):

    def setUp(self):
        self.orig_stdout = sys.stdout
        self.stdout = StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = self.orig_stdout
