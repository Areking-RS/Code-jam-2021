import dataclasses
from typing import Optional


@dataclasses.dataclass
class Component:
    entity: Optional[int] = None

    def with_id(self, _id: int):
        self.entity = _id
        return self
