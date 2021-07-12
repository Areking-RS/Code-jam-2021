from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Component:
    """A component class to be subclassed by entity components."""

    id: int

    def with_id(self, _id: int) -> Component:
        """Assigns an ID to the Component object on the fly."""
        self.id = _id
        return self
