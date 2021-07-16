import asyncio
from typing import Callable, Coroutine, Dict, Optional, Type, TypeVar

from game.ecs.component import Component

_T = TypeVar("_T")
ProcessorFunc = Callable[[float, 'World', str], None]


def _id_generator():
    n = 0
    while True:
        yield n
        n = n + 1


class World(object):
    """
    World class, whose object will hold entities, components and processors.
    """

    entities: set[int]
    components: Dict[Type[_T], Dict[int, Component]]
    processors: set[ProcessorFunc]

    def __init__(self):
        self.id_generator = _id_generator()
        self.entities = set()
        self.components = {}
        self.processors = set()

    def create_entity(self, *components: Component) -> int:
        """
        Create a new entity and assign it an ID.

        :param components: Entity components
        :return: Entity ID
        """
        entity_id = next(self.id_generator)

        self.entities.add(entity_id)
        self.add_components(entity_id, *components)

        return entity_id

    def delete_entity(self, entity_id: int) -> None:
        if entity_id in self.entities:
            # TODO: Could speed this up at the cost of memory by keeping a dict of entity_id -> Set[Type[Component]]
            #       and using that to shortcut looking through each component bucket.
            for component_map in self.components.values():
                if entity_id in component_map:
                    del component_map[entity_id]
            self.entities.discard(entity_id)

    def add_components(self, entity_id: int, *components: Component) -> None:
        """

        :param entity_id: ID of an entity
        :param components: Components to associate
        :return: None
        """
        for component in components:
            c_type = type(component)
            if c_type not in self.components:
                self.components[c_type] = {}
            self.components[c_type][entity_id] = component.with_id(entity_id)

    def get_component(self, entity_id: int, component_type: Type[_T]) -> Optional[_T]:
        if component_type in self.components and entity_id in self.components[component_type]:
            return self.components[component_type][entity_id]
        else:
            return None

    def get_components(self, component_type: Type[_T]) -> list[_T]:
        """
        Returns a list of all components of a matching type.

        :param component_type: Component class type
        :return: List of components
        """
        if component_type in self.components:
            return list(self.components[component_type].values())
        else:
            return []

    def remove_components(self, entity, *components):
        for component in components:
            c_type = type(component)
            try:
                del self.components[c_type][entity]
            except KeyError:
                pass

    def register_processor(self, func: ProcessorFunc) -> None:
        """
        Register a processor.

        :param func: Callable coroutine
        :return: None
        """
        self.processors.add(func)

    def remove_processor(self, func: ProcessorFunc) -> None:
        """
        Remove and unregister a processor.

        :param func: Callable coroutine
        :return: None
        """
        self.processors.discard(func)

    def tick(self, dt, inp: str) -> None:
        """
        Asynchronously process all processors.

        :return: None
        """
        for func in self.processors:
            func(dt, self, inp)
