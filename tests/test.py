import unittest
import time

from progress import ProgressBar


class TestProgressBar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.total = 100
        cls.width = 30
        cls.prefix = "Processing..."

    def test_0(self):
        with ProgressBar(self.total, self.width, self.prefix) as bar:
            for _ in range(self.total):
                bar.update(add=1)
                time.sleep(0.025)
