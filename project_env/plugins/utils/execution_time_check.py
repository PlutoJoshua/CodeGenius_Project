import time

class ElapseTime:
    def __enter__(self):
        self.start = time.time()

    def __exit__(self, type, value, traceback):
        end = time.time()
        print(f"{'=' * 13}\nRUNNING_TIME\n{'=' * 13}\n{round(end - self.start, 2)}초\n{'=' * 13}")