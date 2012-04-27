import silverwing.models
from silverwing.models import Element, Attribute, Schema, Schema_Element, Document, DocumentContent
from silverwing.database import Session, Base, engine

def bootstrap():
    Base.metadata.create_all(engine)
    # exit()

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