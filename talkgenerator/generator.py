import argparse
import os
import pathlib
import random
import subprocess
import sys
import logging
from typing import List, Union

from talkgenerator.schema.content_generators import full_name_generator
from talkgenerator.schema.presentation_schema_types import get_schema
from talkgenerator import runtime_checker
from talkgenerator.sources import phrasefinder
from talkgenerator.util import os_util

DEFAULT_PRESENTATION_TOPIC = "cat"
MAX_PRESENTATION_SAVE_TRIES = 100

logger = logging.getLogger("talkgenerator")


def generate_presentation_using_cli_arguments(args):
    """Make a talk with the given topic."""

    runtime_checker.check_runtime_environment()

    # Print status details
    logger.info("******************************************")
    logger.info("Making {} slide talk on: {}".format(args.num_slides, args.topic))

    return generate_presentation(
        schema=args.schema,
        slides=args.num_slides,
        topic=args.topic,
        title=args.title,
        presenter=args.presenter,
        parallel=args.parallel,
        int_seed=args.int_seed,
        print_logs=args.print_logs,
    )


def generate_presentation(
    schema: str,
    slides: int,
    topic: Union[str, List[str]] = None,
    title: str = None,
    presenter: str = None,
    parallel: bool = True,
    int_seed: int = None,
    save_ppt: bool = True,
    output_folder: str = "../output/",
    open_ppt: bool = False,
    print_logs=False,
):
    if print_logs:
        os_util.show_logs(logger)

    if int_seed is not None:
        random.seed(int_seed)

    # Retrieve the schema to generate the presentation with
    presentation_schema = get_schema(schema)

    # Generate random presenter name if no presenter name given
    if not presenter:
        presenter = full_name_generator()

    if not topic:
        if title:
            topic = phrasefinder.get_rarest_word(title)
        else:
            topic = DEFAULT_PRESENTATION_TOPIC

    # Extract topics from given (possibly comma separated) topic
    if type(topic) in [list, tuple]:
        topics = topic
    else:
        topics = [topic.strip() for topic in topic.split(",")]

    # Generate the presentation object
    presentation, slide_deck = presentation_schema.generate_presentation(
        topics=topics,
        num_slides=slides,
        presenter=presenter,
        title=title,
        parallel=parallel,
        int_seed=int_seed,
    )

    cleaned_topics = ",".join(topics).replace(" ", "").replace(",", "_")
    file_name = "".join(e for e in cleaned_topics if e.isalnum() or e == "_")

    logger.info(
        "Slide deck structured data: {}".format(slide_deck.get_structured_data())
    )

    # Save presentation
    presentation_file = None
    if save_ppt:
        presentation_file = save_presentation_to_pptx(
            output_folder, file_name, presentation
        )

        # Open the presentation
        if open_ppt and presentation_file is not None:
            path = os.path.realpath(presentation_file)
            _open_file(path)

    return presentation, slide_deck, presentation_file


def save_presentation_to_pptx(output_folder: str, file_name: str, prs, index=0):
    """Save the talk."""
    if index > MAX_PRESENTATION_SAVE_TRIES:
        return None

    suffix = "_" + str(index) if index > 0 else ""
    fp = os.path.join(output_folder, str(file_name) + str(suffix) + ".pptx")

    # If file already exists, don't overwrite it:
    if pathlib.Path(fp).is_file():
        return save_presentation_to_pptx(output_folder, file_name, prs, index + 1)

    # Create the parent folder if it doesn't exist
    pathlib.Path(os.path.dirname(fp)).mkdir(parents=True, exist_ok=True)

    try:
        prs.save(fp)
        logger.info("Saved talk to {}".format(fp))
        return fp
    except PermissionError:
        return save_presentation_to_pptx(output_folder, file_name, prs, index + 1)


def _open_file(filename: str):
    """Platform independent open method to cover different OS."""
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def str2bool(v):
    # stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def get_argument_parser():
    parser = argparse.ArgumentParser(description="Quickly build a slide deck.")
    parser.add_argument("--topic", default="", type=str, help="Topic of presentation.")
    parser.add_argument(
        "--num_slides",
        "--slides",
        default=10,
        type=int,
        help="Number of slides to create.",
    )
    parser.add_argument(
        "--int_seed",
        default=None,
        type=int,
        help="Seed used for random.seed(int_seed). Fill in any number to add more consistency between runs.",
    )
    parser.add_argument(
        "--schema",
        default="default",
        type=str,
        help="The presentation schema to generate the presentation with",
    )
    parser.add_argument(
        "--presenter",
        default=None,
        type=str,
        help="The full name of the presenter, leave blank to randomise",
    )
    parser.add_argument(
        "--title",
        default=None,
        type=str,
        help="The title of the talk, leave blank to randomise",
    )
    parser.add_argument(
        "--parallel",
        default=True,
        type=str2bool,
        help=(
            "Generated powerpoint will generate in parallel "
            + "faster but drops some conditions)"
        ),
    )
    parser.add_argument(
        "--print_logs",
        default=True,
        type=str2bool,
        help="Print logs about the generation process.",
    )
    parser.add_argument(
        "--output_folder",
        default="../output/",
        type=str,
        help="The folder to output the generated presentations",
    )
    parser.add_argument(
        "--save_ppt",
        default=True,
        type=str2bool,
        help="If this flag is true, the generated powerpoint will be saved",
    )
    parser.add_argument(
        "--open_ppt",
        default=True,
        type=str2bool,
        help="Generated powerpoint will automatically open",
    )
    return parser
