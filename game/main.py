from blessed import Terminal

from game.state import Intro


def main() -> None:
    """Entrypoint for the game"""
    term = Terminal()

    speed = 1 / 10
    inp = None

    level = Intro()
    level.setup(term)

    with term.hidden_cursor(), term.cbreak(), term.location():
        while inp not in (u'q', u'Q'):
            next_level = level.tick(term, 0.0, inp)
            if next_level is not None:
                level = next_level
                level.setup(term)
            inp = term.inkey(timeout=speed)


if __name__ == '__main__':
    main()
