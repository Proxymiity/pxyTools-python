from time import time


def _time():
    return int(time())


class ObjectCache:
    __slots__ = ("data", "tracker", "lifespan", "name", "hits", "writes", "reads", "tests", "evictions")

    def __len__(self):
        return len(self.data)

    def __init__(self, data=None, tracker=None, lifespan=None, name=None):
        self.data = data or {}
        self.tracker = tracker or {}
        self.lifespan = lifespan or 3600
        self.name = name or "cache"
        self.hits = 0
        self.writes = 0
        self.reads = 0
        self.tests = 0
        self.evictions = 0

    def clear(self):
        print(f"[{self.name}] Clear cache memory.")
        self.__init__(name=self.name, lifespan=self.lifespan)

    def store(self, request, response):
        print(f"[{self.name}] Storing {request} at {_time()}")
        self.writes += 1
        self.data[request] = response
        self.tracker[request] = _time()
        return response

    def read(self, request):
        print(f"[{self.name}] Reading {request}")
        self.hits += 1
        self.reads += 1
        return self.data.get(request)

    def cached(self, request):
        self.tests += 1
        return request in self.data

    def evict(self, request, force: bool = False):
        if _time() > self.tracker.get(request, 0) + self.lifespan or force:
            self.evictions += 1
            self.data.pop(request)
            self.tracker.pop(request)
            print(f"[{self.name}] Evicting {request}")

    def evict_scan(self):
        for x in self.tracker:
            if _time() > self.tracker.get(x, 0) + self.lifespan:
                self.evictions += 1
                self.data.pop(x)
                self.tracker.pop(x)
                print(f"[{self.name}] Evicting {x}")
