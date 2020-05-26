import os
from urllib.parse import parse_qs

from dotenv import load_dotenv
from slack import WebClient
from tornado.options import define, options, parse_command_line
import tornado.web
import tornado.ioloop

from tasks import savequote, quote

# Load environment variables
load_dotenv()

slack_web_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))


# Define possible command line arguments to pass
# when run tornado server
define(
    name='port',
    default=8000,
    help='Port to run the server',
    type=int
)
define(
    name='debug',
    default=False,
    help='To run the app in debug mode. ONLY USE IT IN DEV MODE'
)
define(
    name='autoreload',
    default=False,
    help='App will watch for changes in source files and reload it automatically'
)


class MainHandler(tornado.web.RequestHandler):
    """Test if api is working"""

    def get(self):
        self.write({
            'ok': True,
            'message': 'Slack bot is working'
        })


class SaveQuoteCommandHandler(tornado.web.RequestHandler):
    """Handle the request to slack command /savequote"""

    def post(self):
        # Slack need to know if the server is proccessing the
        # request, to inform that we send a 200 status code
        self.set_status(200)

        # Get data sent by slack in request object
        bytes_data = self.request.body

        # Decoded data to transform it into a dict
        decoded_data = bytes_data.decode('utf-8')
        payload = parse_qs(decoded_data)

        # Get data from user that triggered the commnad
        user_name = payload['user_name'][0]
        quote = payload['text'][0]

        data_to_save = {
            'author': user_name,
            'quote': quote
        }

        savequote.delay(data=data_to_save)


class QuoteHandler(tornado.web.RequestHandler):
    """Handle the request for slack command /quote"""

    def post(self):
        # Slack need to know if the server is proccessing the
        # request, to inform that we send a 200 status code
        self.set_status(200)

        # Get data sent by slack in request object
        bytes_data = self.request.body

        # Decoded data to transform it into a dict
        decoded_data = bytes_data.decode('utf-8')
        payload = parse_qs(decoded_data)

        # Get data from user that triggered the commnad
        channel_id = payload['channel_id'][0]

        # Run the task to get a random quote
        response = quote.delay().ready()

        print(response)


def main():
    """Run the http server"""
    parse_command_line()
    app = tornado.web.Application(
        # Routes
        [
            (r'/', MainHandler),
            (r'/api/quote', QuoteHandler),
            (r'/api/savequote', SaveQuoteCommandHandler),
        ],
        # Settings
        debug=options.debug,
        autoreload=options.autoreload
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
