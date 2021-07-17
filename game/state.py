from typing import Generator, Optional, Union

from blessed import Terminal

from game.components import (
    Ascii, Movement, PlayerInput, Renderable, Text, TimeToLive, Transform
)
from game.cutscenes import CutsceneFrame, CutsceneSequence, ordered_cutscenes
from game.ecs.world import World
from game.mapgeneration import MapType, mapgenerator
from game.processors import (
    ascii_renderer, input_processor, movement_processor, render_system,
    text_renderer, ttl_processor
)
from game.utils import Vector2, echo


def _level_progression() -> Generator[Union['Cutscene', 'GameLevel'], None, None]:
    for cutscene in ordered_cutscenes:
        yield Cutscene(cutscene)

        next_map, spawn = mapgenerator(
            map_width=50,
            map_height=50,
            room_frequency=10,
            room_size=30,
            path_width=5
        )
        yield GameLevel(next_map, spawn)
    # TODO: Once we're out of levels, spawn a credits or some story ending


# This generator outputs our level progression
story_progression = _level_progression()


class Screen(object):
    """Base class for all game screens"""

    def __init__(self, world: Optional[World] = None):
        if world is None:
            world = World()
        self.world = world

    def setup(self, term: Terminal) -> None:
        """
        Run setup for the screen before beginning ticks.

        :param term: Terminal reference for running setup operations
        :return: None
        """
        pass

    def tick(self, term: Terminal, dt: float, inp: str) -> Optional['Screen']:
        """
        Tick (update) the screen

        :param term: Terminal reference
        :param dt: Delta between game loop iterations
        :param inp: Keyboard input
        :return: Optional next screen
        """
        # TODO: Globally before any processors run, blanking the screen makes some sense
        #       but it may not always be appropriate
        color_bg = term.on_blue
        echo(term.move_yx(0, 0))
        echo(color_bg(term.clear))
        self.world.tick(term, dt, inp)
        return None


class Intro(Screen):
    """Intro screen for the game"""

    def __init__(self):
        super(Intro, self).__init__()
        self.text_entity: Optional[int] = None
        self.ttl_component: Optional[TimeToLive] = None

    def setup(self, term: Terminal) -> None:
        """
        Run setup for the screen before beginning ticks.

        :param term: Terminal reference for running setup operations
        :return: None
        """
        text = Text(text_string='Dedicated Dugongs', v_align=Text.VerticalAlign.CENTER)
        self.ttl_component = TimeToLive(expires_after=1)
        self.text_entity = self.world.create_entity(text, self.ttl_component)
        self.world.register_processor(text_renderer)
        self.world.register_processor(ttl_processor)

    def tick(self, term: Terminal, dt: float, inp: str) -> Optional['Screen']:
        """
        Tick (update) the screen

        :param term: Terminal reference
        :param dt: Delta between game loop iterations
        :param inp: Keyboard input
        :return: Optional next screen
        """
        # TODO: Blank the screen
        super(Intro, self).tick(term, dt, inp)
        if self.ttl_component.expired:
            return next(story_progression)


class GameLevel(Screen):
    """Screen that plays out a game level"""

    def __init__(self, level: MapType, spawn_location: int):
        super(GameLevel, self).__init__()
        self.level = level
        self.spawn_location = spawn_location

    def setup(self, term: Terminal) -> None:
        """
        Run setup for the screen before beginning ticks.

        :param term: Terminal reference for running setup operations
        :return: None
        """
        self.world.register_processor(input_processor)

        self.world.create_entity(
            Transform(position=Vector2(x=self.spawn_location)),
            Movement(direction=Vector2.RIGHT),
            PlayerInput(),
            Renderable(w=1, h=1, character=u'^')
        )

        self.world.register_processor(movement_processor(self.level))
        self.world.register_processor(render_system(self.level))

    def tick(self, term: Terminal, dt: float, inp: str) -> Optional['Screen']:
        """
        Tick (update) the screen

        :param term: Terminal reference
        :param dt: Delta between game loop iterations
        :param inp: Keyboard input
        :return: Optional next screen
        """
        try:
            super(GameLevel, self).tick(term, dt, inp)
        except IndexError:
            next_screen = next(story_progression)
            return next_screen


class Cutscene(Screen):
    """A screen that handles displaying cutscenes"""

    def __init__(self, sequence: CutsceneSequence):
        super(Cutscene, self).__init__()
        self.sequence: CutsceneSequence = sequence
        self.ascii: Optional[Ascii] = None
        self.art_ttl: Optional[TimeToLive] = None
        self.text: Optional[Text] = None

    def _next_scene(self) -> Optional[CutsceneFrame]:
        """
        Get the next frame of the cutscene

        :return: The CutsceneFrame or None if there are no more frames
        """
        try:
            return self.sequence.pop(0)
        except IndexError:
            return None

    def setup(self, term: Terminal) -> None:
        """
        Run setup for the screen before beginning ticks.

        :param term: Terminal reference for running setup operations
        :return: None
        """
        scene = self._next_scene()

        if scene is None:
            raise ValueError('Cutscene empty on setup')

        art, timing, text = scene
        self.ascii = Ascii(art=art)
        self.art_ttl = TimeToLive(expires_after=timing)
        self.text = Text(text_string=text)

        self.world.create_entity(
            self.ascii,
            self.art_ttl,
            self.text
        )

        self.world.register_processor(text_renderer)
        self.world.register_processor(ttl_processor)
        self.world.register_processor(ascii_renderer)

    def tick(self, term: Terminal, dt: float, inp: str) -> Optional['Screen']:
        """
        Tick (update) the screen

        :param term: Terminal reference
        :param dt: Delta between game loop iterations
        :param inp: Keyboard input
        :return: Optional next screen
        """
        super(Cutscene, self).tick(term, dt, inp)
        if self.art_ttl.expired:
            scene = self._next_scene()
            if scene is None:
                next_screen = next(story_progression)
                return next_screen

            # Switch out the frame data on the components
            art, timing, text = scene
            self.ascii.art = art
            self.art_ttl.expires_after = timing
            self.art_ttl.start_time = None
            self.art_ttl.current_time = None
            self.text.text_string = text
