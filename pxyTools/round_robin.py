class RoundRobin:
    def __init__(self, items, name=None):
        self.name = name or "rr"
        self.items = items
        self.next_item = 0

    def next(self):
        self.next_item = 0 if len(self.items) == self.next_item + 1 else self.next_item + 1
        print(f"[{self.name}] #{self.next_item - 1}")
        return self.items[self.next_item - 1]

    n = next
