from tornado.web import HTTPError, RequestHandler
from .database import Session
from .models import Element, Attribute, Schema, Document
from .gists import FlashMessageMixin
from .util import DotExpandedDict
from pprint import pprint
    
class IndexHandler(RequestHandler):
    def get(self):
        self.redirect('/documents')
        
class DocumentsHandler(RequestHandler):
    def get(self, action=None):
        if action:
            document = Document(name='')
            try:
                session = Session()
                document = session.query(Document).filter(Document.id == action).one()
            except:
                pass
            self.render('documents_edit.html', document=document)
        else:
            session = Session()
            documents = session.query(Document).all()
            self.render('documents.html', documents=documents)
        
class SchemasHandler(RequestHandler):
    def get(self, action=None):
        if action:
            schema = Schema(name='')
            try:
                session = Session()
                schema = session.query(Schema).filter(Schema.id == action).one()
            except:
                pass
            self.render('schemas_edit.html', schema=schema)
        else:
            session = Session()
            schemas = session.query(Schema).all()
            self.render('schemas.html', schemas=schemas)
        
class ElementsHandler(RequestHandler, FlashMessageMixin):
    def get(self, action=None):
        if action:
            m = self.get_flash_message('m')
            element = Element(name='', pyclass='', attributes=[])
            try:
                session = Session()
                element = session.query(Element).filter(Element.id == action).one()
            except:
                pass
            self.render('elements_edit.html', element=element, m=m)
        else:
            session = Session()
            elements = session.query(Element).all()
            self.render('elements.html', elements=elements)
            
    def post(self, action):
        session = Session()
        element = Element(name='', pyclass='', attributes=[])
        try:
            element = session.query(Element).filter(Element.id == action).one()
        except:
            element = Element()
            session.add(element)
        element.name = self.get_argument('name')
        element.pyclass = self.get_argument('pyclass', '')
        element.attributes = []
        expanded = DotExpandedDict(self.request.arguments)
        if 'attrs' in expanded:
            for item in expanded['attrs'].values():
                name = item['name'][0] if 'name' in item else None
                type = item['type'][0] if 'type' in item else 'value'
                defaultVal = item['default'][0] if 'default' in item else ''
                if not name:
                    continue
                attr = Attribute(name=name)
                if type == 'value':
                    attr.defaultValue = defaultVal
                else:
                    attr.defaultText = defaultVal
                element.attributes.append(attr)
        session.commit()
        self.set_flash_message('m', 'Saved')
        self.redirect('/elements/%s' % action)

    def delete(self, action):
        session = Session()
        element = Element(name='', pyclass='', attributes=[])
        try:
            element = session.query(Element).filter(Element.id == action).one()
            session.delete(element)
            session.commit()
        except:
            raise
        
class AttributesHandler(RequestHandler):
    def delete(self):
        pass
     
class VuzeHandler(RequestHandler):
    """Prevent Vuze discovery service noise in console"""
    def get(self):
        pass
