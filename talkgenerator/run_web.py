import json
import pprint

from flask import Flask
from flask import request

from talkgenerator.utils import generate_talk
from talkgenerator.utils import get_argument_parser
from talkgenerator.utils import notify_error

app = Flask(__name__)

argparser = get_argument_parser()

HTTP_ERROR_CLIENT = 403
HTTP_ERROR_SERVER = 500


@app.route('/gen', methods=['GET'])
def talkgen_generate():
    """ When this route is called with a GET request check the topic and the
    number of slides in the calling URL and then process from there.

    Example: http://0.0.0.0:5687/gen?topic=chairs&slides=2

    This would generate a presentation about chairs with 2 slides.
    """

    #validate the inputs from the request
    slides = None
    topic = ''
    if 'topic' not in request.args or request.args['topic'] in ("", None):
        return notify_error("ERR_NO_ARG:  'topic' argument required", HTTP_ERROR_CLIENT)
    topic = request.args.get('topic', '')

    if 'slides' not in request.args or request.args['slides'] in ("", None):
        return notify_error("ERR_NO_ARG:  'slides' argument required", HTTP_ERROR_CLIENT)

    if 'slides' in request.args and request.args['slides'] not in ("0", None):
        try:
            slides = int(request.args.get('slides', ''))
        except:
            return notify_error("ERR_NO_ARG:  'slides' must be an integer", HTTP_ERROR_CLIENT)

        if slides < 1 or slides > 15:
            return notify_error("ERR_OUT_OF_BOUNDS:  'slides' parameger must be between 1 and 15", HTTP_ERROR_CLIENT)

    args = argparser.parse_args(gather_run_params(topic, slides))
    try:
        generate_talk(args)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    except Exception as ex:
        return notify_error(ex, HTTP_ERROR_SERVER)

# Create argparsable list of params to run against the run.main
def gather_run_params(topic, slides):
    if topic in ("", None):
        print('No topic given, using a random word.')
        topic = random_word_util.random_word()

    num_slides = str(slides)
    return ['--topic', topic,
    '--num_slides', num_slides,
    '--open_ppt', 'false']

class LoggingMiddleware(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, environ, resp):
        errorlog = environ['wsgi.errors']
        pprint.pprint(('REQUEST', environ), stream=errorlog)

        def log_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)

        return self._app(environ, log_response)

def startup_web():
    app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run(host="0.0.0.0", port=5687)

if __name__=='__main__':
    startup_web()
