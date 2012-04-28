import tornado
import tornado.ioloop
from tornado.options import options
import os

from silverwing.handlers import IndexHandler, DocumentsHandler, SchemasHandler
from silverwing.handlers import ElementsHandler, AttributesHandler, VuzeHandler
import silverwing.uimethods
from silverwing.util import load_options
from silverwing.bootstrap import bootstrap

load_options()

if options.bootstrap:
    bootstrap()
    exit()

root = os.path.abspath(os.path.dirname(__file__))  
settings = {
    'static_path': os.path.join(root, 'static'),
    'template_path': os.path.join(root, 'templates'),
    'ui_methods': silverwing.uimethods,
    'cookie_secret': options.cookie_secret,
    'autoescape': None,
    'debug': options.debug
}

routes = [
    (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static'}),
    (r"/announce", VuzeHandler),
    (r"/scrape", VuzeHandler),
    (r"/documents/?", DocumentsHandler),
    (r"/documents/(.[^/]*)/?", DocumentsHandler),
    (r"/schemas/?", SchemasHandler),
    (r"/schemas/(.[^/]*)/?", SchemasHandler),
    (r"/elements/?", ElementsHandler),
    (r"/elements/(.[^/]*)/?", ElementsHandler),
    (r"/attributes/\d+/?", AttributesHandler),
    (r"/.*", IndexHandler)
]
            
if __name__ == '__main__':
    application = tornado.web.Application(routes, **settings)
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
