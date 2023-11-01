import hashlib
import multiprocessing


class MD5HashFinder:
    def __init__(self, target_hash, start_value=0, end_value=10000000000):
        self.target_hash = target_hash
        self.num_processes = max(multiprocessing.cpu_count() - 7, 1)
        self.start_value = start_value
        self.end_value = end_value
        self.chunk_size = (end_value - start_value) // self.num_processes

    def md5_hash_matches(self, start, end, process_complete_event):
        for i in range(start, end):
            input_string = f"{i:010}"
            hash_attempt = hashlib.md5(input_string.encode()).hexdigest()
            if hash_attempt == self.target_hash:
                print(input_string)
                print(f"Process {multiprocessing.current_process().name} found the original input: {input_string}")
                process_complete_event.set()  # Signal that the process has completed
                return

    def find_original_input(self):
        process_list = []

        process_complete_events = [multiprocessing.Event() for _ in range(self.num_processes)]

        for process_number in range(self.num_processes):
            start = self.start_value + process_number * self.chunk_size
            end = start + self.chunk_size if process_number < self.num_processes - 1 else self.end_value
            process = multiprocessing.Process(
                target=self.md5_hash_matches,
                args=(start, end, process_complete_events[process_number])
            )
            process_list.append(process)
            process.start()

        # Wait for any process to complete
        any(process_event.wait() for process_event in process_complete_events)

        # Terminate the remaining processes
        for process in process_list:
            if process.is_alive():
                process.terminate()

        print("All processes have finished")


if __name__ == "__main__":
    target_hash = "EC9C0F7EDCC18A98B1F31853B1813301"
    hash_finder = MD5HashFinder(target_hash)
    hash_finder.find_original_input()
