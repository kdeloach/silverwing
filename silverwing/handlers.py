from tornado.web import HTTPError, RequestHandler
from .database import Session
from .models import Element, Attribute, Schema, Document
    
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
        
class ElementsHandler(RequestHandler):
    def get(self, action=None):
        if action:
            element = Element(name='', pyclass='', attributes=[])
            try:
                session = Session()
                element = session.query(Element).filter(Element.id == action).one()
            except:
                pass
            self.render('elements_edit.html', element=element)
        else:
            session = Session()
            elements = session.query(Element).all()
            self.render('elements.html', elements=elements)
        
class VuzeHandler(RequestHandler):
    """Prevent Vuze discovery service noise in console"""
    def get(self):
        pass
