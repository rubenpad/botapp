import os

from slack import WebClient
from tornado.options import define, options, parse_command_line
import tornado.web
import tornado.ioloop

from tasks import greeting

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
    """Send a hello world message"""

    def get(self):
        greeting.delay('anyone')
        self.write({
            'ok': True,
            'message': 'Slack bot is working'
        })


class SaveQuoteCommandHandler(tornado.web.RequestHandler):
    """Handle actions when an user call the command savequote"""

    def post(self):
        print(self.request)


def main():
    """Run the http server"""
    parse_command_line()
    app = tornado.web.Application(
        # Routes
        [
            (r'/', MainHandler),
            (r'/api/savequote', SaveQuoteCommandHandler)
        ],
        # Settings
        debug=options.debug,
        autoreload=options.autoreload
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
