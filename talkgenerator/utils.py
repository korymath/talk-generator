import argparse
import datetime
import logging
import os
import pathlib
import subprocess
import sys
import logging

from flask import jsonify
from flask import request

from talkgenerator import settings
from talkgenerator.schema import schemas
from talkgenerator.sources import phrasefinder

DEFAULT_PRESENTATION_TOPIC = 'cat'
MAX_PRESENTATION_SAVE_TRIES = 100

logger = logging.getLogger("talkgenerator")


def generate_talk(args):
    """Make a talk with the given topic."""

    if args.print_logs:
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Print status details
    logger.info('******************************************')
    logger.info("Making {} slide talk on: {}".format(
        args.num_slides, args.topic))
    logger.info("S3 Enabled: {}".format(settings.AWS_S3_ENABLED))

    # Retrieve the schema to generate the presentation with
    schema = schemas.get_schema(args.schema)

    # Generate random presenter name if no presenter name given
    if not args.presenter:
        args.presenter = schemas.full_name_generator()

    if not args.topic:
        if args.title:
            args.topic = phrasefinder.get_rarest_word(args.title)
        else:
            args.topic = DEFAULT_PRESENTATION_TOPIC

    # Extract topics from given (possibly comma separated) topic
    args.topics = [topic.strip() for topic in args.topic.split(',')]

    # Generate random talk title
    if not args.title or args.title is None:
        args.title = schemas.talk_title_generator({'seed': args.topics[0]})

    # Generate the presentation object
    presentation, slide_deck = schema.generate_presentation(
        topics=args.topics,
        num_slides=args.num_slides,
        presenter=args.presenter,
        title=args.title,
        parallel=args.parallel)

    cleaned_topics = args.topic.replace(' ', '').replace(',', '_')
    file_name = ''.join(e for e in cleaned_topics if e.isalnum() or e == '_')

    logger.info('Slide deck structured data: {}'.format(
        slide_deck.get_structured_data()))

    # Save presentation
    if args.save_ppt or settings.AWS_S3_ENABLED:
        presentation_file = save_presentation_to_pptx(
            args.output_folder, file_name, presentation)

        # Open the presentation
        if args.open_ppt and presentation_file is not None:
            path = os.path.realpath(presentation_file)
            open_file(path)

        if settings.AWS_S3_ENABLED:
            from talkgenerator.util import aws_s3
            logger.info("Saving slides to S3 key {}".format(file_name + ".pptx"))
            # if aws_s3.check_for_object(settings.BUCKET, args.topic):
            aws_s3.store_file(bucket=settings.BUCKET,
                              key=args.topic + ".pptx",
                              file=os.path.realpath(presentation_file))
    return presentation, slide_deck


def save_presentation_to_pptx(output_folder, file_name, prs, index=0):
    """Save the talk."""
    if index > MAX_PRESENTATION_SAVE_TRIES:
        return None

    suffix = "_" + str(index) if index > 0 else ""
    fp = os.path.join(output_folder, str(file_name) + str(suffix) + ".pptx")

    # If file already exists, don't overwrite it:
    if pathlib.Path(fp).is_file():
        return save_presentation_to_pptx(
            output_folder, file_name, prs, index + 1)

    # Create the parent folder if it doesn't exist
    pathlib.Path(os.path.dirname(fp)).mkdir(parents=True, exist_ok=True)

    try:
        prs.save(fp)
        logger.info('Saved talk to {}'.format(fp))
        return fp
    except PermissionError:
        return save_presentation_to_pptx(
            output_folder, file_name, prs, index + 1)


def open_file(filename):
    """Platform independent open method to cover different OS."""
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


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
    parser.add_argument('--topic', default='', type=str,
                        help="Topic of presentation.")
    parser.add_argument('--num_slides', '--slides', default=10, type=int,
                        help="Number of slides to create.")
    parser.add_argument('--schema', default="default", type=str,
                        help="The presentation schema to generate the presentation with")
    parser.add_argument('--presenter', default=None, type=str,
                        help="The full name of the presenter, leave blank to randomise")
    parser.add_argument('--title', default=None, type=str,
                        help="The title of the talk, leave blank to randomise")
    parser.add_argument('--parallel', default=True, type=str2bool,
                        help=("Generated powerpoint will generate in parallel " +
                              "faster but drops some conditions)"))
    parser.add_argument('--print_logs', default=True, type=str2bool,
                        help="Print logs about the generation process.")
    parser.add_argument('--output_folder', default="../output/", type=str,
                        help="The folder to output the generated presentations")
    parser.add_argument('--save_ppt', default=True, type=str2bool,
                        help="If this flag is true, the generated powerpoint will be saved")
    parser.add_argument('--open_ppt', default=True, type=str2bool,
                        help="Generated powerpoint will automatically open")
    return parser


def log_api_call(func):
    """
    function:  log_api_call

    params:    function this decorator is decorating.

    returns:   function that being wrapped.  The inner wrapped function is optionally logging api calls and returns the result of the function being wrapped.

    notes:      This decorator function may be applied to any flask api call.  The idea is that if a "Apitrace" header value is supplied, then this can be output
                to a log.  This is useful for clients using multiple micro services and want to trace transactions through all of them.
                Currently using the default flask log.  Could be easily augmented to log to centralized syslog, RabbitMQ, or any other mechanism.

    examples:

              -- The code

              @log_api_call
              @app.route('/fibonacci/foo', methods=['GET'])
              def fibonacci_foo_api():
                   do something interesting...

              -- The client
              curl -H "Apitrace: 1232345346" http://localhost:5000/fibonacci/foo

              -- Output to logs:
              API CALL: fibonacci_foo_api TRACE: 1232345346
    """

    def log_api_call_wrapper(*args, **kwargs):
        if 'Apitrace' in request.headers and request.headers['Apitrace'] is not None:
            log = logging.getLogger('werkzeug')
            log.info("%s | API CALL: %s TRACE: %s " % (
                str(datetime.datetime.now()), func.__name__, request.headers['Apitrace']))
        return func(*args, **kwargs)

    return log_api_call_wrapper


def notify_error(msg, status_code):
    """
    function:  notify_error

    params:    msg - message to send back to the client.
               status_code - http status code to send to the client.

    returns:   flask response object suitable for return to the client.  Will have an "error" key with the message from our caller.

    notes:     Common status codes for client side problems:  https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_Error
               Common status codes for server side problems:  https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#5xx_Server_Error

    examples:

    if 'count' not in request.args:
        return notify_error("'count' argument required to /fibonacci/api", 403)

    """
    resp = jsonify(error=str(msg))
    resp.status_code = status_code
    return resp
