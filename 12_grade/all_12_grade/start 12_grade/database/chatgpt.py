import json
import threading
import multiprocessing
import os

class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.D_data = {}
        self.lock = threading.Lock() if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.Lock()

        # Load data from the file if it exists
        if os.path.isfile(self.file_path):
            with open(self.file_path, 'r') as json_file:
                self.D_data = json.load(json_file)

    def set_value(self, key, data):
        with self.lock:
            self.D_data[key] = data
            with open(self.file_path, 'w') as json_file:
                json.dump(self.D_data, json_file, indent=4, separators=(',', ': '))

    def get_value(self, key):
        with self.lock:
            return self.D_data.get(key, "Key not found")

    def delete_value(self, key):
        with self.lock:
            if key in self.D_data:
                value = self.D_data.pop(key)
                with open(self.file_path, 'w') as json_file:
                    json.dump(self.D_data, json_file, indent=4, separators=(',', ': '))
                return value
            return None

class Commands:
    def __init__(self, type_, file_path):
        self.fm = FileManager(file_path)

    def add_data(self):
        key = input("Enter the key: ")
        data = input("Enter the data: ")
        self.fm.set_value(key, data)

    def get_data(self):
        key = input("Enter the key: ")
        return self.fm.get_value(key)

    def delete_data(self):
        key = input("Enter the key to delete: ")
        return self.fm.delete_value(key)

class ThreadManger(Commands):
    def __init__(self, file_path):
        super().__init__("thread", file_path)
        self.threads_ = []

    def commands(self):
        running = True
        while running:
            command = input("Enter the command you want to do from the list [Add | Get | Remove | Quit]: ")

            if command.lower() == "add":
                self.add_data()

            elif command.lower() == "get":
                print(self.get_data())

            elif command.lower() == "remove":
                result = self.delete_data()
                if result is not None:
                    print(f"Deleted value: {result}")
                else:
                    print("Key not found.")

            elif command.lower() == "quit":
                running = False

    def start_threads(self):
        for i in range(10):
            t = threading.Thread(target=self.commands, daemon=True)
            self.threads_.append(t)
        for t in self.threads_:
            t.start()

class MultiManger(Commands):
    def __init__(self, file_path):
        super().__init__("multi", file_path)
        self.multi_ = []

    def commands(self):
        c_ = Commands("multi", self.fm.file_path)
        running = True
        while running:
            command = input("Enter the command you want to do from the list [Add | Get | Remove | Quit]: ")

            if command.lower() == "add":
                c_.add_data()

            elif command.lower() == "get":
                print(c_.get_data())

            elif command.lower() == "remove":
                result = c_.delete_data()
                if result is not None:
                    print(f"Deleted value: {result}")
                else:
                    print("Key not found.")

            elif command.lower() == "quit":
                running = False

    def start_processes(self):
        for i in range(10):
            p = multiprocessing.Process(target=self.commands, daemon=True)
            self.multi_.append(p)
        for p in self.multi_:
            p.start()

def main():
    file_path = "data.json"
    thm = ThreadManger(file_path)
    mm = MultiManger(file_path)

    thm_thread = threading.Thread(target=thm.start_threads, daemon=True)
    mm_process = multiprocessing.Process(target=mm.start_processes, daemon=True)

    thm_thread.start()
    mm_process.start()

    thm_thread.join()
    mm_process.join()

if __name__ == "__main__":
    main()
