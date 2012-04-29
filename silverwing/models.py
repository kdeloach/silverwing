from datetime import datetime
from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import and_
from .database import Base
from .util import get_class

class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    version = Column(Integer, default=1)
    schema_id = Column(Integer, ForeignKey('schema.id'))
    created = Column(DateTime, default=datetime.utcnow)
    schema = relationship('Schema')
    contents = relationship('DocumentContent',
                    primaryjoin=lambda: and_(Document.id == DocumentContent.document_id, 
                        Document.version == DocumentContent.version))

class DocumentContent(Base):
    __tablename__ = 'documentcontent'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('document.id'))
    schema_element_id = Column(Integer, ForeignKey('schema_element.id'))
    attribute_id = Column(Integer, ForeignKey('attribute.id'))
    version = Column(Integer)
    value = Column(String(100))
    text = Column(Text)
    document = relationship('Document')
    schema_element = relationship('Schema_Element')
    attribute = relationship('Attribute')
    
class Schema(Base):
    __tablename__ = 'schema'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    version = Column(Integer, default=1)
    created = Column(DateTime, default=datetime.utcnow)
    elements = relationship('Schema_Element')
   
class Schema_Element(Base):
    __tablename__ = 'schema_element'
    id = Column(Integer, primary_key=True)
    schema_id = Column(Integer, ForeignKey('schema.id'))
    element_id = Column(Integer, ForeignKey('element.id'))
    name = Column(String(40))
    title = Column(String(40))
    element = relationship('Element')
   
class Element(Base):
    __tablename__ = 'element'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('element.id'))
    name = Column(String(40))
    pyclass = Column(String(40))
    created = Column(DateTime, default=datetime.utcnow)
    attributes = relationship('Attribute', backref='element', order_by=lambda: Attribute.name)
    elements = relationship('Element')
    
    def getAttributes(self):
        """Return supported attrs; Ignore non-supported attrs"""
        if not self.pyclass:
            return self.attributes
        inst = get_class(self.pyclass)
        validattrs = [a.name for a in inst.attrs]
        result = []
        for a in self.attributes:
            if a.name in validattrs:
                result.append(a)
                validattrs.remove(a.name)
        result += [Attribute(name=a, defaultValue='') for a in validattrs]
        return result
        
    def jsonObj(self):
        return dict(id=self.id,
                    name=self.name,
                    pyclass=self.pyclass,
                    attributes=[a.jsonObj() for a in self.getAttributes()],
                    elements=[e.jsonObj() for e in self.elements])
    
class Attribute(Base):
    __tablename__ = 'attribute'
    id = Column(Integer, primary_key=True)
    element_id = Column(Integer, ForeignKey('element.id'))
    name = Column(String(40))
    defaultValue = Column(String(100))
    created = Column(DateTime, default=datetime.utcnow)
    
    def jsonObj(self):
        return dict(id=self.id,
                    name=self.name,
                    defaultValue=self.defaultValue)
    
class Template(Base):
    __tablename__ = 'template'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    created = Column(DateTime, default=datetime.utcnow)
    

    
    
    
    