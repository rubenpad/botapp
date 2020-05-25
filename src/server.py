from tornado.options import define, options, parse_command_line
import tornado.web
import tornado.ioloop

from tasks import greeting


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
        self.write('Hello')


def make_app():
    """Creates a tornado app"""
    return


def main():
    """Run the http server"""
    parse_command_line()
    app = tornado.web.Application(
        # Routes
        [
            (r'/', MainHandler),
        ],
        # Settings
        debug=options.debug,
        autoreload=options.autoreload
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
