class Component:
    id: int

    def with_id(self, _id: int):
        self.id = _id
        return self

    def __str__(self):
        return f"{dir(self)}"

    def __repr__(self):
        return self.__str__()
