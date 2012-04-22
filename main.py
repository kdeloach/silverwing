import tornado
import tornado.ioloop
from tornado.options import options
import os

from silverwing.handlers import IndexHandler, DocumentsHandler, SchemasHandler, ElementsHandler, VuzeHandler
import silverwing.uimethods
from silverwing.util import load_options

load_options()

if options.bootstrap:
    import silverwing.models
    from silverwing.database import Session, Base, engine
    Base.metadata.create_all(engine)
    # exit()
    
    from silverwing.models import Element, Attribute, Schema, Schema_Element, Document, DocumentContent
    session = Session()
    # elements
    text = Element(name='Text', pyclass='silverwing.elements.Text')
    textContent = Attribute(name='content')
    text.attributes.append(textContent)
    session.add(text)
    textBox = Element(name='TextBox', pyclass='silverwing.elements.TextBox')
    textBoxContent = Attribute(name='content')
    textBox.attributes.append(textBoxContent)
    session.add(textBox)
    # schemas
    basic = Schema(name='Basic', version=1)
    title = Schema_Element(name='title', title='Title', element=text)
    basic.elements.append(title)
    content = Schema_Element(name='content', title='Content', element=textBox)
    basic.elements.append(content)
    session.add(basic)
    # documents
    page1 = Document(name='Page 1', version=2, schema=basic)
    page1.contents.append(DocumentContent(schema_element=title, attribute=textContent, value='old page title', version=1))
    page1.contents.append(DocumentContent(schema_element=content, attribute=textBoxContent, text='old page content', version=1))
    page1.contents.append(DocumentContent(schema_element=title, attribute=textContent, value='new page title', version=2))
    page1.contents.append(DocumentContent(schema_element=content, attribute=textBoxContent, text='new page content', version=2))
    session.add(page1)
    session.commit()
    
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
    (r"/.*", IndexHandler)
]
            
if __name__ == '__main__':
    application = tornado.web.Application(routes, **settings)
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
