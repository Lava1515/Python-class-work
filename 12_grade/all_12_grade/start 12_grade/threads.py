import threading


class Work:
    def __init__(self):
        self.num = None

    def Worker(self):
        print("work" + str(self.num))


def main():
    worker = Work()
    for i in range(5):
        worker.num = 1
        t = threading.Thread(target=worker.Worker)
        t.start()


if __name__ == "__main__":
    main()
