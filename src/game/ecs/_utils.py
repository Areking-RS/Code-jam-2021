from typing import Iterator


class _IDGenerator:
    n = 0

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        result = self.n
        self.n += 1
        return result


id_generator = _IDGenerator()
