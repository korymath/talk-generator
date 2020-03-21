from talkgenerator import talkgenerator


def main(args):
    """Main run method for command line talk generation."""
    presentations, slide_deck = talkgenerator.generate_talk(args)


def main_cli():
    args = talkgenerator._get_argument_parser().parse_args()
    main(args)


if __name__ == "__main__":
    main(talkgenerator._get_argument_parser().parse_args())
