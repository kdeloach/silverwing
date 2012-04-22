import os
import os.path

def partial(handler, name, **kwargs):
    filename = os.path.join(handler.settings['template_path'], name.replace(':', os.sep))
    if os.path.exists(filename):
        return handler.render_string(filename, **kwargs)
    return handler.render_string('System/PageNotExist', name=name)
    
def iif(handler, cond, a):
    if cond:
        return a
        
def v(handler, str):
    if not str:
        return ''
    return str