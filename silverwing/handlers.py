from tornado.web import HTTPError, RequestHandler
from .database import Session
from .elements import BaseElement
from .gists import FlashMessageMixin
from .models import Element, Attribute, Schema, Document
from .util import DotExpandedDict, inheritors
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
            # list of all element classes and attributes
            classes = [Element(pyclass=cls.__module__ + '.' + cls.__name__, \
                attributes=[Attribute(name=a.name, defaultValue='') for a in cls.attrs]) for cls in inheritors(BaseElement)]
            # list of all element id's and name's to use on Group Element dropdowns
            elements = [Element(id=id, name=name) for (id, name) in \
                session.query(Element).filter(Element.id != action).values(Element.id, Element.name)]
            self.render('elements_edit.html', element=element, elements=elements, classes=classes, m=m)
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
            for name in expanded['attrs']:
                item = expanded['attrs'][name]
                attr = Attribute(name=name)
                attr.defaultValue = item[0]
                element.attributes.append(attr)
        session.commit()
        self.set_flash_message('m', 'Saved')
        self.redirect('/elements/%s' % element.id)

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
