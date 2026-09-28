from __future__ import annotations

from copy import deepcopy
from threading import Lock
from typing import Any


class SharedMemory:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.store = {}
        return cls._instance

    def set(self, key: str, value: Any) -> None:
        self.store[key] = deepcopy(value)

    def get(self, key: str, default: Any = None) -> Any:
        return deepcopy(self.store.get(key, default))

    def update(self, key: str, value: Any) -> None:
        current = self.store.get(key, {})
        if isinstance(current, dict) and isinstance(value, dict):
            current.update(value)
            self.store[key] = current
        else:
            self.store[key] = deepcopy(value)

    def delete(self, key: str) -> None:
        self.store.pop(key, None)

    def all(self) -> dict[str, Any]:
        return deepcopy(self.store)


memory = SharedMemory()


def get_memory() -> SharedMemory:
    return memory

