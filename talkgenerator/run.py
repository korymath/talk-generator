from talkgenerator import talkgenerator


def main(args):
    """Main run method for command line talk generation."""
    presentations, slide_deck = talkgenerator.generate_presentation_using_cli_arguments(
        args
    )


def main_cli():
    args = talkgenerator.get_argument_parser().parse_args()
    main(args)


if __name__ == "__main__":
    main_cli()
