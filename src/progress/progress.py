import time
import shutil
import threading


class ProgressBar:
    """
    Progress bar

    Attributes:
        total: int
            Total number of steps.
        width: int
            Width of the progress bar.
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
        self.endTime = None
        self.autoUpdateThread: threading.Thread = None
        self.stopThread: bool = False
        self.lock = threading.Lock()
        self.pastLength = 0

    def __enter__(self):
        if self.allowAutoPrint:
            self.autoUpdateThread = threading.Thread(target=self.autoUpdate)
            self.autoUpdateThread.start()
        with self.lock:
            self.printBar()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.autoUpdateThread is not None:
            self.stopAutoUpdateThread()
        self.stop()

    def update(self, set: int = None, add: int = 0, prefix: str = None):
        """
        Update the progress bar.
        If set is not None, set the progress bar to the given value.
        If add is not None, add the given value to the progress bar.

        Args:
            add: int
                Add the given value to the progress bar.
            set: int
                Set the progress bar to the given value.
            prefix: str
                Set the prefix of the progress bar.
        """
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

    def reset(
        self, total: int, width: int = 30, prefix: str = "Processing..."
    ):
        """
        Reset the progress bar.

        Args:
            total: int
                Total number of steps.
            width: int
                Width of the progress bar.
            prefix: str
                Prefix of the progress bar.
        """
        self.total = total
        self.width = width
        self.prefix = prefix
        self.cnt = 0
        self.startTime = time.time()
        self.endTime = None

    def stop(self):
        self.endTime = time.time()
        if self.cnt < self.total:
            print(flush=True)

    def stopAutoUpdateThread(self):
        self.stopThread = True
        self.autoUpdateThread.join()

    def autoUpdate(self):
        time.sleep(0.5)
        while not self.stopThread:
            if self.cnt != self.total:
                with self.lock:
                    self.printBar()
            time.sleep(0.5)

    def printBar(self):
        col, _ = shutil.get_terminal_size((0, 20))

        totalTime = time.time() - self.startTime
        try:
            averageTime = self.cnt / (time.time() - self.startTime)
        except ZeroDivisionError:
            averageTime = 0
        try:
            leftTime = (self.total - self.cnt) / averageTime
        except ZeroDivisionError:
            leftTime = 0

        percent = int(self.cnt / self.total * 100)

        l = self.width * percent // 100
        r = self.width - l

        barStr = (
            "\r| ",
            self.prefix,
            " |",
            "█" * l,
            " " * r,
            "|",
            f" {percent}% - {self.cnt} / {self.total}",
            " | total: {:.2f}s".format(totalTime),
            " | avg: {:.2f}/s".format(averageTime),
            " | left: {:.2f}s".format(leftTime),
            " |",
        )
        barStr = "".join(barStr)
        barLen = len(barStr)
        lastSpace = 0
        if self.pastLength > barLen:
            lastSpace = (
                self.pastLength - barLen
                if self.pastLength - barLen < col - barLen
                else col - barLen
            )

        print(barStr, " " * lastSpace, sep="", end="", flush=True)

        self.pastLength = barLen

        if self.cnt == self.total:
            print()


if __name__ == "__main__":
    total = 100
    width = 30
    prefix = "Processing..."

    print("enter progress bar")

    with ProgressBar(total, width, prefix) as bar:
        for _ in range(total):
            bar.update(add=1)
            time.sleep(0.05)

    with ProgressBar(total, width, prefix) as bar:
        for i in range(total):
            bar.update(add=1)
            if i == 0:
                time.sleep(5)
            else:
                time.sleep(0.001)

    with ProgressBar(total, width, prefix) as bar:
        try:
            cnt = 0
            offset = 1
            while True:
                bar.update(set=cnt)
                cnt += offset
                if cnt >= total - 1:
                    offset = -1
                if cnt <= 1:
                    offset = 1
                time.sleep(0.01)
        except KeyboardInterrupt:
            pass

    print("exit progress bar")
