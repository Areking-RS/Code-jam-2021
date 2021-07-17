from typing import Callable, NewType

from blessed import Terminal

EntityId = NewType('EntityId', int)
ProcessorFunc = Callable[[Terminal, 'World', float, str], None]  # noqa: F821
