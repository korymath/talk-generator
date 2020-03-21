from talkgenerator import talkgenerator_main


def main(args):
    """Main run method for command line talk generation."""
    presentations, slide_deck = talkgenerator_main.generate_talk(args)


def main_cli():
    args = talkgenerator_main.get_argument_parser().parse_args()
    main(args)


if __name__ == "__main__":
    main(talkgenerator_main.get_argument_parser().parse_args())
