import unittest
import time

from progress import ProgressBar


class TestProgressBar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.total = 100
        cls.width = 30
        cls.prefix = "Testing..."

    def setUp(self):
        print()

    def test_0_update_add(self):
        with ProgressBar(self.total, self.width, self.prefix) as bar:
            for _ in range(self.total):
                bar.update(add=1)
                time.sleep(0.025)

    def test_1_update_set(self):
        with ProgressBar(self.total, self.width, self.prefix) as bar:
            for i in range(self.total + 1):
                bar.update(set=i)
                time.sleep(0.025)

    def test_2_raise_value_error(self):
        with self.assertRaises(ValueError):
            with ProgressBar(self.total, self.width, self.prefix) as bar:
                bar.update(set=1, add=1)

    def test_3_raise_value_error(self):
        with self.assertRaises(ValueError):
            with ProgressBar(self.total, self.width, self.prefix) as bar:
                bar.update()

    def test_4_reset(self):
        with ProgressBar(self.total, self.width, self.prefix) as bar:
            for _ in range(self.total):
                bar.update(add=1)
                time.sleep(0.001)

            test_prefix = "Reseted..."

            bar.reset(prefix=test_prefix)

            self.assertEqual(bar.cnt, 0)
            self.assertEqual(bar.endTime, None)
            self.assertEqual(bar.prefix, test_prefix)
            self.assertEqual(bar.width, self.width)
            self.assertEqual(bar.total, self.total)

            for _ in range(self.total):
                bar.update(add=1)
                time.sleep(0.001)

    def test_5_long_time(self):
        with ProgressBar(self.total, self.width, self.prefix) as bar:
            for i in range(self.total):
                bar.update(add=1)
                if i == 0 or i == 50:
                    time.sleep(2)
                else:
                    time.sleep(0.001)

    def test_6_infinite_width(self):
        with ProgressBar(self.total, -1, self.prefix) as bar:
            for _ in range(self.total):
                bar.update(add=1)
                time.sleep(0.025)

    def test_7_chinese(self):
        prefix = "中文測試..."
        with ProgressBar(self.total, self.width, prefix) as bar:
            for _ in range(self.total):
                bar.update(add=1)
                time.sleep(0.025)

    def test_8_chinese_infinite_width(self):
        prefix = "中文測試..."
        with ProgressBar(self.total, -1, prefix) as bar:
            for _ in range(self.total):
                bar.update(add=1)
                time.sleep(0.025)
