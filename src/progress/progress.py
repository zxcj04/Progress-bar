import time
import sys
import shutil


class ProgressBar:
    def __init__(self, total, width=30, prefix="Processing..."):
        self.total = total
        self.width = width
        self.prefix = prefix
        self.cnt = 0
        self.startTime = time.time()
        self.endTime = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def update(self, add, prefix=None):
        self.cnt += add
        if prefix is not None:
            self.prefix = prefix
        self.printBar()

    def setCnt(self, cnt):
        self.cnt = cnt
        self.printBar()

    def stop(self):
        self.endTime = time.time()
        if self.cnt < self.total:
            print()
            sys.stdout.flush()

    def printBar(self):
        col, _ = shutil.get_terminal_size((80, 20))

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
        print(
            "\r",
            " " * col,
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
            sep="",
            end=" |",
        )
        sys.stdout.flush()

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
        try:
            cnt = 0
            offset = 1
            while True:
                bar.setCnt(cnt)
                cnt += offset
                if cnt >= total - 1:
                    offset = -1
                if cnt <= 1:
                    offset = 1
                time.sleep(0.01)
        except KeyboardInterrupt:
            pass

    print("exit progress bar")
