import asyncio
from typing import Callable, Coroutine, Type, TypeVar

from ._component import Component
from ._utils import id_generator

_T = TypeVar("_T")


class World:
    """
    World class, whose object will hold entities, components and processors.
    """

    entities: set[int]
    components: list[Component]
    processors: set[Callable[[], Coroutine]]

    def __init__(self):
        self.entities = set()
        self.components = []
        self.processors = set()

    def _append_components(self, entity_id: int, *components: Component):
        self.components += [component.with_id(entity_id) for component in components]

    def create_entity(self, *components: Component) -> int:
        """
        Create a new entity and assign it an ID.

        :param components: Entity components
        :return: Entity ID
        """
        entity_id = next(id_generator)

        self.entities.add(entity_id)
        self._append_components(entity_id, *components)

        return entity_id

    def delete_entity(self, entity_id: int) -> None:
        if entity_id in self.entities:
            indexes_to_pop: list[int] = []
            for i, component in enumerate(self.components):
                if component.id == entity_id:
                    indexes_to_pop.append(i)

            for i in indexes_to_pop:
                self.components.pop(i)

            self.entities.discard(entity_id)

    def add_components(self, entity_id: int, *components: Component) -> None:
        """

        :param entity_id: ID of an entity
        :param components: Components to associate
        :return: None
        """
        if entity_id not in self.entities:
            raise ValueError(f"Entity `{entity_id}` not found.")

        self._append_components(entity_id, *components)

    def get_components(self, component_type: Type[_T]) -> list[_T]:
        """
        Returns a list of all components of a matching type.

        :param component_type: Component class type
        :return: List of components
        """
        return [component for component in self.components if issubclass(type(component), component_type)]

    def register_processor(self, func: Callable[[], Coroutine]) -> None:
        """
        Register a processor.

        :param func: Callable coroutine
        :return: None
        """
        self.processors.add(func)

    def remove_processor(self, func: Callable[[], Coroutine]) -> None:
        """
        Remove and unregister a processor.

        :param func: Callable coroutine
        :return: None
        """
        self.processors.discard(func)

    async def tick(self) -> None:
        """
        Asynchronously process all processors.

        :return: None
        """
        await asyncio.gather(*[func() for func in self.processors])
