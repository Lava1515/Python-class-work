import json
import threading
from os import path
import multiprocessing


class DataBase:
    def __init__(self, D_data=None):
        if D_data is None:
            D_data = {}
        self.D_data = D_data

    def set_value(self, key_, data_):
        self.D_data[key_] = data_

    def get_value(self, key_):
        if key_ in self.D_data:
            return self.D_data[key_]
        return "key not found"

    def delete_value(self, key_):
        if key_ in self.D_data:
            value = self.D_data.pop(key_)
            return value
        return None


class FileManager(DataBase):
    def __init__(self):
        self.file_path = "data.json"
        D_data = {}
        try:
            with open(self.file_path) as f:
                D_data = json.load(f)
        except Exception:
            pass
        super().__init__(D_data)
        self.T_lock = threading.Lock

    def set_value(self, key_, data_):
        if path.isfile(self.file_path) is False:
            raise Exception("File not found")
        super().set_value(key_, data_)
        with open(self.file_path, 'w') as json_file:
            json.dump(self.D_data, json_file,
                      indent=4,
                      separators=(',', ': '))

    def delete_value(self, key_):
        if path.isfile(self.file_path) is False:
            raise Exception("File not found")
        super().delete_value(key_)
        with open(self.file_path, 'w') as json_file:
            json.dump(self.D_data, json_file,
                      indent=4,
                      separators=(',', ': '))


class Commands:
    def __init__(self, type_):
        self.lock = None
        self._semaphore = None
        self.max_readers = 10
        self.fm = FileManager()
        if type_ == "thread":
            self.lock = threading.Lock()
            self._semaphore = threading.Semaphore(self.max_readers)
        elif type_ == "multi":
            self.lock = multiprocessing.Lock()
            self._semaphore = multiprocessing.Semaphore(self.max_readers)

    def add_data(self):
        key = input("the you want to add")
        data = input("the data you want to add to the key")
        self.lock.acquire()
        for _ in range(self.max_readers):
            self._semaphore.acquire()
        self.fm.set_value(key, data)
        self.lock.release()
        for _ in range(self.max_readers):
            self._semaphore.release()

    def get_data(self):
        key = input("the you want to get")
        self.lock.acquire()
        for _ in range(self.max_readers):
            self._semaphore.acquire()
        x = self.fm.get_value(key)
        self.lock.release()
        for _ in range(self.max_readers):
            self._semaphore.release()
        return x

    def delete_data(self):
        key = input("the you want to remove")
        self.lock.acquire()
        for _ in range(self.max_readers):
            self._semaphore.acquire()
            for _ in range(self.max_readers):
                self._semaphore.acquire()
        self.fm.delete_value(key)
        self.lock.release()
        for _ in range(self.max_readers):
            self._semaphore.release()

    def commands(self):
        running = True
        while running:
            command = input("Enter the command you want to do from the list "
                            "[Add | Get | Remove | quit]")

            if command.lower() == "add":
                self.add_data()

            elif command.lower() == "get":
                print(self.get_data())

            elif command.lower() == "remove":
                self.delete_data()

            elif command.lower() == "quit":
                running = False


class ThreadManger(Commands):
    def __init__(self):
        super().__init__("thread")
        self.threads_ = []

    def start_threads(self):
        for i in range(10):
            t = threading.Thread(target=self.commands, daemon=True)
            self.threads_.append(t)
        for t in self.threads_:
            t.start()
            t.join()


class MultiManger(Commands):
    def __init__(self):
        super().__init__("multi")
        self.multi_ = []

    def start_process(self):
        for i in range(10):
            p = multiprocessing.Process(target=self.commands, daemon=True)
            self.multi_.append(p)
        for p in self.multi_:
            p.start()
            p.join()


def main():
    thm = ThreadManger()
    thm.start_threads()


if __name__ == "__main__":
    main()
