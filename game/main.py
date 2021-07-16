from blessed import Terminal

from game.components import Movement, PlayerInput, Renderable, Transform
from game.ecs.world import World
from game.mapgeneration import mapgenerator
from game.processors import input_processor, movement_processor, render_system
from game.state import Intro
from game.utils import Vector2


def main():
    term = Terminal()

    speed = 1/10
    inp = None


    level = Intro()
    level.setup(term)


    # Thread(target=game_loop).start()
    with term.hidden_cursor(), term.cbreak(), term.location():
        while inp not in (u'q', u'Q'):
            next_level = level.tick(term, 0.0, inp)
            if next_level is not None:
                print('Changing levels')
                level = next_level
                level.setup(term)
            inp = term.inkey(timeout=speed)


if __name__ == '__main__':
    main()
