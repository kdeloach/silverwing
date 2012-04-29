from collections import namedtuple
from .util import get_class, load_options
from tornado.template import Loader
from tornado.options import options

load_options()

class BaseElement(object):
    attrs = []
    
    def __init__(self, dbelem):
        self.dbelem = dbelem
    
    def render(self, vals):
        pass
        
    def renderTemplate(self, filename, **kwargs):
        loader = template.Loader(options.template_path)
        return loader.load(filename).generate(**kwargs)
            
Attribute = namedtuple('Attribute', ['name', 'column'])

class Group(BaseElement):
    attrs = [
        Attribute(name='template', column='value')
    ]
    
    def render(self, vals):
        return self.renderTemplate('group.html', dbelem=self.dbelem, vals=vals)
        # for elem in self.dbelem.elements:
        #   inst = get_class(elem.pyclass)
        #   inst(elem).render(vals)
            
class Text(BaseElement):
    attrs = [
        Attribute(name='content', column='value')
    ]
    
    def render(self, vals):
        return self.renderTemplate('text.html', dbelem=self.dbelem, vals=vals)
    
class TextBox(BaseElement):
    attrs = [
        Attribute(name='content', column='text'),
        Attribute(name='truncate', column='value')
    ]
    
    def render(self, vals):
        return self.renderTemplate('textbox.html', dbelem=self.dbelem, vals=vals)
