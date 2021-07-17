import dataclasses
from typing import Optional

from game.ecs import EntityId


@dataclasses.dataclass
class Component:
    """Base class for all components"""

    entity: Optional[EntityId] = None

    def with_id(self, _id: EntityId) -> 'Component':
        """
        Associate an entity with this component

        :param _id: ID of the entity this component is associated with
        :return: Same component
        """
        self.entity = _id
        return self
