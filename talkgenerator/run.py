import os
from talkgenerator import utils
from talkgenerator import runtime_check


def main(args):
    """Main run method for command line talk generation."""
    presentations, slide_deck = utils.generate_talk(args)


def main_cli():
    args = utils.get_argument_parser().parse_args()
    main(args)


if __name__ == '__main__':
    main(utils.get_argument_parser().parse_args())
