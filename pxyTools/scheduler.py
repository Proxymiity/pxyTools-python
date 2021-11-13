from time import time, sleep
from threading import Thread


def _time():
    return int(time())


class TimeScheduler:
    __slots__ = ("name", "checkInterval", "pendingOperations", "started", "thread", "auto")

    def __init__(self, name=None, interval: int = 1, pending: dict = None, auto: bool = True):
        self.name = name or "scheduler"
        self.checkInterval = interval
        self.pendingOperations = pending or {}
        self.started = False
        self.thread = None
        self.auto = auto

    def set(self, identifier, callback, args: list = None, kwargs: dict = None,
            time_left: int = None, time_set: int = None):
        if time_left:
            expected_time = _time() + time_left
        elif time_set:
            expected_time = time_set
        else:
            raise Exception("No schedule method selected. Use either time_left or time_set arguments.")
        self.pendingOperations[identifier] = (expected_time, callback, args, kwargs)
        print(f"[{self.name}] Added operation {identifier}")
        if self.auto:
            self._auto()

    def set_time(self, identifier, time_left: int = None, time_set: int = None):
        _op = self.pendingOperations[identifier]
        if time_left:
            expected_time = _time() + time_left
        elif time_set:
            expected_time = time_set
        else:
            raise Exception("No schedule method selected. Use either time_left or time_set arguments.")
        self.pendingOperations[identifier] = (expected_time, _op[1], _op[2], _op[3])
        print(f"[{self.name}] Set time for operation {identifier}")

    def set_time_relative(self, identifier, relative_time: int = None):
        _op = self.pendingOperations[identifier]
        self.pendingOperations[identifier] = (_op[0] + relative_time, _op[1], _op[2], _op[3])
        print(f"[{self.name}] Set time for operation {identifier}")

    def remove(self, identifier):
        if identifier in self.pendingOperations:
            print(f"[{self.name}] Removing operation {identifier}")
            return self.pendingOperations.pop(identifier)
        if self.auto:
            self._auto()

    def is_pending(self, identifier):
        if identifier in self.pendingOperations:
            return True
        else:
            return False

    def _target(self):
        while self.started is True:
            _to_remove = []
            _operations = self.pendingOperations.copy()
            for x in _operations:
                _op = _operations[x]
                if _op[0] <= _time():
                    print(f"[{self.name}] Processing {x}...")
                    _to_remove.append(x)
                    try:
                        if _op[2] is not None:
                            o = _op[1](*_op[2])
                        elif _op[3] is not None:
                            o = _op[1](**_op[3])
                        else:
                            o = _op[1]()
                    except Exception as e:
                        print(f"[{self.name}] {x} failed with error {e}")
                    else:
                        print(f"[{self.name}] {x} succeeded with output {o}")
            for y in _to_remove:
                self.pendingOperations.pop(y)
            if self.auto:
                self._auto()
            sleep(self.checkInterval)

    def start(self):
        self.started = True
        self.thread = Thread(target=self._target)
        self.thread.start()
        print(f"[{self.name}] Started scheduler thread")

    def stop(self):
        self.started = False
        print(f"[{self.name}] Stopped scheduler thread")

    def _auto(self):
        if self.pendingOperations and not self.started:
            self.start()
        elif not self.pendingOperations and self.started:
            self.stop()


class BucketScheduler:
    __slots__ = ("name", "bucketMidInterval", "pendingOperations", "defaultOperationTimer", "started", "thread", "auto")

    def __init__(self, name=None, interval: int = 0, timer: int = 1, pending: list = None, auto: bool = True):
        self.name = name or "scheduler"
        self.bucketMidInterval = interval
        self.defaultOperationTimer = timer
        self.pendingOperations = pending or []
        self.started = False
        self.thread = None
        self.auto = auto

    def add(self, callback, timer: int = None, args: list = None, kwargs: dict = None):
        timer = timer or self.defaultOperationTimer
        self.pendingOperations.append((timer, callback, args, kwargs))
        print(f"[{self.name}] Queued new operation")
        if self.auto:
            self._auto()

    def clear(self):
        self.pendingOperations = []
        print(f"[{self.name}] Cleared operation queue")
        if self.auto:
            self._auto()

    def _target(self):
        while self.started is True:
            if self.pendingOperations:
                _op = self.pendingOperations[0]
                print(f"[{self.name}] Processing operation...")
                try:
                    if _op[2] is not None:
                        o = _op[1](*_op[2])
                    elif _op[3] is not None:
                        o = _op[1](**_op[3])
                    else:
                        o = _op[1]()
                except Exception as e:
                    print(f"[{self.name}] Operation failed with error {e}")
                else:
                    print(f"[{self.name}] Operation succeeded with output {o}")
                self.pendingOperations.pop(0)
                sleep(_op[0])
            if self.auto:
                self._auto()
            sleep(self.bucketMidInterval)

    def start(self):
        self.started = True
        self.thread = Thread(target=self._target)
        self.thread.start()
        print(f"[{self.name}] Started bucket thread")

    def stop(self):
        self.started = False
        print(f"[{self.name}] Stopped bucket thread")

    def _auto(self):
        if self.pendingOperations and not self.started:
            self.start()
        elif not self.pendingOperations and self.started:
            self.stop()
