import os
import os.path
from .util import tojson as js

def partial(handler, name, **kwargs):
    filename = os.path.join(handler.settings['template_path'], name.replace(':', os.sep))
    if os.path.exists(filename):
        return handler.render_string(filename, **kwargs)
    return handler.render_string('System/PageNotExist', name=name)
    
def iif(handler, cond, a, b=''):
    if cond:
        return a
    else:
        return b
        
def v(handler, str):
    if not str:
        return ''
    return str
    
def htmlselectoptions(handler, opts, selected=None):
    """opts is a list of tuples containing value/name pairs"""
    result = ''
    for k, v in opts:
        result += '<option value="%s"' % k
        if k == selected:
            result += ' selected="selected"'
        result += '>%s</option>' % v
    return result
        
def tojson(handler, obj):
    return js(obj)