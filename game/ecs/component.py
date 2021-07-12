import dataclasses
from typing import Optional


@dataclasses.dataclass
class Component:
    entity: Optional[int] = None

    def with_id(self, _id: int):
        self.entity = _id
        return self

    def __str__(self):
        return f"{dir(self)}"

    def __repr__(self):
        return self.__str__()
