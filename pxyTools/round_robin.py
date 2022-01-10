class RoundRobin:
    def __init__(self, items, name=None):
        self.name = name or "rr"
        self.items = items
        self.item = 0

    def next(self):
        self.item = 0 if len(self.items) == self.item + 1 else self.item + 1
        print(f"[{self.name}] #{self.item}")
        return self.items[self.item]

    n = next
