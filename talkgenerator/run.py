import os
import sys
import pathlib
import argparse
import subprocess

sys.path.insert(0, os.path.abspath('..'));

from talkgenerator import settings
from talkgenerator.schema import schemas

MAX_PRESENTATION_SAVE_TRIES = 100


def _save_presentation_to_pptx(output_folder, file_name, prs, index=0):
    """Save the talk."""
    if index > MAX_PRESENTATION_SAVE_TRIES:
        return None

    suffix = "_" + str(index) if index > 0 else ""
    fp = os.path.join(output_folder, str(file_name) + str(suffix) + ".pptx")

    # If file already exists, don't overwrite it:
    if pathlib.Path(fp).is_file():
        return _save_presentation_to_pptx(
            output_folder, file_name, prs, index + 1)

    # Create the parent folder if it doesn't exist
    pathlib.Path(os.path.dirname(fp)).mkdir(parents=True, exist_ok=True)

    try:
        prs.save(fp)
        print('Saved talk to {}'.format(fp))
        return fp
    except PermissionError:
        return _save_presentation_to_pptx(
            output_folder, file_name, prs, index + 1)


def open_file(filename):
    """Platform independent open method to cover different OS."""
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def main(arguments):
    """Make a talk with the given topic."""
    # Print status details
    print('******************************************')
    print("Making {} slide talk on: {}".format(
        arguments.num_slides, arguments.topic))
    print("S3 Enabled: {}".format(settings.AWS_S3_ENABLED))

    # Retrieve the schema to generate the presentation with
    schema = schemas.get_schema(arguments.schema)

    # Generate random presenter name if no presenter name given
    if not arguments.presenter:
        arguments.presenter = schemas.full_name_generator()

    # Generate the presentation object
    presentation = schema.generate_presentation(topic=arguments.topic,
                                                num_slides=arguments.num_slides,
                                                presenter=arguments.presenter,
                                                parallel=arguments.parallel)

    # Save presentation
    if arguments.save_ppt or settings.AWS_S3_ENABLED:
        presentation_file = _save_presentation_to_pptx(
            arguments.output_folder, arguments.topic, presentation)

        # Open the presentation
        if arguments.open_ppt and presentation_file is not None:
            path = os.path.realpath(presentation_file)
            open_file(path)

        if settings.AWS_S3_ENABLED:
            from server import aws_s3
            print("Saving slides to S3 key {}".format(
                arguments.topic + ".pptx"))
            # if aws_s3.check_for_object(settings.BUCKET, arguments.topic):
            aws_s3.store_file(bucket=settings.BUCKET,
                              key=arguments.topic + ".pptx",
                              file=os.path.realpath(presentation_file))
    return presentation


def str2bool(v):
    # stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_argument_parser():
    parser = argparse.ArgumentParser(description='Quickly build a slide deck.')
    parser.add_argument('--topic', default='cat', type=str,
        help="Topic of presentation.")
    parser.add_argument('--num_slides', default=10, type=int,
        help="Number of slides to create.")
    parser.add_argument('--schema', default="default", type=str,
        help="The presentation schema to generate the presentation with")
    parser.add_argument('--presenter', default=None, type=str,
        help="The full name of the presenter, leave blank to randomise")
    parser.add_argument('--parallel', default=True, type=str2bool,
        help=("Generated powerpoint will generate in parallel " +
              "faster but drops some conditions)"))
    parser.add_argument('--output_folder', default="../output/", type=str,
        help="The folder to output the generated presentations")
    parser.add_argument('--save_ppt', default=True, type=str2bool,
        help="If this flag is true, the generated powerpoint will be saved")
    parser.add_argument('--open_ppt', default=True, type=str2bool,
        help="Generated powerpoint will automatically open")
    return parser


if __name__ == '__main__':
    args = get_argument_parser().parse_args()
    main(args)
