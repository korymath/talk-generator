import os
from talkgenerator import utils


def main(args):
    """Main run method for command line talk generation."""
    presentations, slide_deck = utils.generate_talk(args)


if __name__ == '__main__':
    main(utils.get_argument_parser().parse_args())
