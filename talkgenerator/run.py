import os
import sys

from utils import open_file
from utils import generate_talk
from utils import get_argument_parser
from utils import save_presentation_to_pptx


def main(args):
    """Main run method for command line talk generation."""
    presentations, slide_deck = generate_talk(args)


if __name__ == '__main__':
    args = get_argument_parser().parse_args()
    generate_talk(args)
