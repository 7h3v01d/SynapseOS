# modules/core/working_memory_queue.py

class WorkingMemoryQueue:
    def __init__(self, max_items=50):
        self.memory = []
        self.max_items = max_items

    def store(self, item):
        """
        Store a new item in working memory.
        """
        if len(self.memory) >= self.max_items:
            self.memory.pop(0)
        self.memory.append(item)
        print(f"[💾] Memory stored: {item}")

    def recall_all(self):
        """
        Return all items in memory.
        """
        return self.memory

    def recall_last(self, n=3):
        """
        Return the last n memory items.
        """
        return self.memory[-n:] if len(self.memory) >= n else self.memory
