class _IDGenerator:
    n = 0

    def __iter__(self):
        return self

    def __next__(self):
        result = self.n
        self.n += 1
        return result


id_generator = _IDGenerator()
