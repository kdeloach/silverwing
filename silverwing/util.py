import tornado
from tornado.options import options, define
import os
import simplejson
from pprint import pprint

# Source: http://stackoverflow.com/a/452981/40
def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m
    
# Source: http://stackoverflow.com/a/5883218/40
def inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses
    
def load_options():
    if 'dsn' in options:
        return
    root = os.path.join(os.path.dirname(__file__), '../')
    define('port', default=80)
    define('debug', default=True, help='enables logging to console')
    define('cookie_secret')
    define('dsn', help='database connection string')
    define('echosql', help='output sql to console', default=True)
    define('bootstrap', help='rebuild database and default values', default=False)
    define('static_path')
    define('template_path')
    tornado.options.parse_config_file(os.path.join(root, 'site.conf'))
    tornado.options.parse_command_line()
    
# Source: Django
class DotExpandedDict(dict):
    """
    A special dictionary constructor that takes a dictionary in which the keys
    may contain dots to specify inner dictionaries. It's confusing, but this
    example should make sense.

    >>> d = DotExpandedDict({'person.1.firstname': ['Simon'], \
            'person.1.lastname': ['Willison'], \
            'person.2.firstname': ['Adrian'], \
            'person.2.lastname': ['Holovaty']})
    >>> d
    {'person': {'1': {'lastname': ['Willison'], 'firstname': ['Simon']}, '2': {'lastname': ['Holovaty'], 'firstname': ['Adrian']}}}
    >>> d['person']
    {'1': {'lastname': ['Willison'], 'firstname': ['Simon']}, '2': {'lastname': ['Holovaty'], 'firstname': ['Adrian']}}
    >>> d['person']['1']
    {'lastname': ['Willison'], 'firstname': ['Simon']}

    # Gotcha: Results are unpredictable if the dots are "uneven":
    >>> DotExpandedDict({'c.1': 2, 'c.2': 3, 'c': 1})
    {'c': 1}
    """
    def __init__(self, key_to_list_mapping):
        for k, v in key_to_list_mapping.items():
            current = self
            bits = k.split('.')
            for bit in bits[:-1]:
                current = current.setdefault(bit, {})
            # Now assign value to current position
            try:
                current[bits[-1]] = v
            except TypeError: # Special-case if current isn't a dict.
                current = {bits[-1]: v}

def jsonencoder(obj):
    """Needed to encode complex objects for JSON reponses"""
    if(hasattr(obj, 'jsonObj')):
        return obj.jsonObj()
    if(hasattr(obj, '__dict__')):
        return obj.__dict__
    return None
    
def tojson(obj):
    return simplejson.dumps(obj, default=jsonencoder)