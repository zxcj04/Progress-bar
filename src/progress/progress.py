import warnings
import time
import shutil
import threading
import unicodedata


LINE_UP = "\x1b[F"
LINE_DOWN = "\x1b[E"
LINE_CLEAR = "\x1b[2K"


class ProgressBar:
    """
    Progress bar

    Attributes:
        total: int
            Total number of steps.
        width: int
            Width of the progress bar.

            if width == -1, the progress bar will be as long as the terminal.
        prefix: str
            Prefix of the progress bar.
        allowAutoPrint: bool
            Whether to allow auto print the progress bar frequently.

    Methods:
        update(set=None, add=None):
            Update the progress bar.
            If set is not None, set the progress bar to the given value.
            If add is not None, add the given value to the progress bar.
        reset(total, width=30, prefix="Processing..."):
            Reset the progress bar.

    Examples:
        >>> from progress import ProgressBar
        >>> with ProgressBar(100, 30, "Processing...") as bar:
        ...     for i in range(100):
        ...         bar.update(set=i)
        ...         time.sleep(0.025)
    """

    def __init__(
        self,
        total: int,
        width: int = 30,
        prefix: str = "Processing...",
        allowAutoPrint: bool = True,
    ):
        self.total = total
        self.width = width
        self.prefix = prefix
        self.allowAutoPrint = allowAutoPrint
        self.cnt = 0
        self.startTime = time.time()
        self.isStop: bool = False
        self.endTime = None
        self.autoPrintThread: threading.Thread = None
        self.isAutoPrintStop: bool = False
        self.lock = threading.Lock()

    def __enter__(self):
        print(flush=True)
        if self.allowAutoPrint:
            self.autoPrintThread = threading.Thread(target=self.autoPrint)
            self.autoPrintThread.start()
        with self.lock:
            self.printBar()
        self.startTime = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.isStop:
            return
        self.stop()

    def update(self, set: int = None, add: int = 0, prefix: str = None):
        """
        Update the progress bar.
        If set is not None, set the progress bar to the given value.
        If add is not None, add the given value to the progress bar.
        If prefix is not None, set the prefix of the progress bar.

        If counter reaches the total, the progress bar will be stopped.

        Args:
            add: int
                Add the given value to the progress bar.
            set: int
                Set the progress bar to the given value.
            prefix: str
                Set the prefix of the progress bar.
        """
        if self.isStop:
            warnings.warn("Progress bar has been stopped, do nothing...")
            return

        if add == 0 and set is None:
            raise ValueError("add or set must be set")
        if prefix is not None:
            self.prefix = prefix
        if set is not None:
            if add != 0:
                raise ValueError("set and add cannot be used at the same time")
            self.cnt = set
        else:
            self.cnt += add
        with self.lock:
            self.printBar()
        if self.cnt >= self.total:
            self.stop()

    def reset(self, total: int = None, width: int = None, prefix: str = None):
        """
        Reset the progress bar.
        If total is None, keep the same total.
        If width is None, keep the same width.
        If prefix is None, keep the same prefix.

        Args:
            total: int
                Total number of steps.
            width: int
                Width of the progress bar.
            prefix: str
                Prefix of the progress bar.
        """
        if total is None:
            total = self.total
        if width is None:
            width = self.width
        if prefix is None:
            prefix = self.prefix.decode("utf8")
        self.stopAutoPrintThread()
        self.__init__(total, width, prefix)
        print(flush=True)
        if self.allowAutoPrint:
            self.autoPrintThread = threading.Thread(target=self.autoPrint)
            self.autoPrintThread.start()

    def stop(self):
        if self.isStop:
            warnings.warn("Progress bar has been stopped, do nothing...")
            return
        self.endTime = time.time()
        self.isStop = True
        self.stopAutoPrintThread()

    def stopAutoPrintThread(self):
        if self.autoPrintThread is None:
            return
        self.isAutoPrintStop = True
        self.autoPrintThread.join()

    def autoPrint(self):
        time.sleep(0.5)
        while not self.isAutoPrintStop:
            if self.cnt != self.total:
                with self.lock:
                    self.printBar()
            time.sleep(0.5)

    @staticmethod
    def wide_chars(s):
        return sum(
            unicodedata.east_asian_width(x) == "W"
            or unicodedata.east_asian_width(x) == "A"
            for x in s
        )

    def fallback_len(self, percent, finalLen):
        template = "| {:s} |{:s}{:s}| {:d}% "
        basicStr = template.format(self.prefix, "", "", percent)
        basicStrLen = len(basicStr)
        return finalLen - basicStrLen

    def printBar(self):
        if self.isStop:
            warnings.warn("Progress bar has been stopped, do nothing...")
            return

        col, _ = shutil.get_terminal_size((0, 20))

        totalTime = time.time() - self.startTime
        try:
            averageRate = self.cnt / totalTime
        except ZeroDivisionError:
            averageRate = 0
        try:
            leftTime = (self.total - self.cnt) / averageRate
        except ZeroDivisionError:
            leftTime = 0

        percent = int(self.cnt / self.total * 100)

        barTemplate = "\r| {:s} |{:s}{:s}| {:d}% - {:d} / {:d} | TTL / ETA: {:.2f}s / {:.2f}s | AVG: {:.2f}/s |"
        finalLen = col - self.wide_chars(self.prefix) + 1

        if self.width == -1:
            barStr = barTemplate.format(
                self.prefix,
                "",
                "",
                percent,
                self.cnt,
                self.total,
                totalTime,
                leftTime,
                averageRate,
            )
            barLen = len(barStr) + self.wide_chars(self.prefix)
            width = col - barLen

            if width <= 0:
                width = self.fallback_len(percent, finalLen)
        else:
            width = self.width

        l = width * percent // 100
        r = width - l

        barStr = barTemplate.format(
            self.prefix,
            "█" * l,
            " " * r,
            percent,
            self.cnt,
            self.total,
            totalTime,
            leftTime,
            averageRate,
        )
        finalStr = "{0:<{1}s}".format(barStr[:finalLen], finalLen)

        print(LINE_UP, finalStr, LINE_DOWN, end="", sep="", flush=True)


if __name__ == "__main__":
    total = 100
    width = 30
    prefix = "Processing..."

    print("enter progress bar")

    with ProgressBar(total, width, prefix) as bar:
        try:
            cnt = 0
            offset = 1
            while True:
                bar.update(set=cnt)
                cnt += offset
                if cnt >= total - 1:
                    offset = -1
                if cnt <= 0:
                    offset = 1
                time.sleep(0.01)
        except KeyboardInterrupt:
            pass

    print("exit progress bar")
