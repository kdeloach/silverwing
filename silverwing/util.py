import tornado
from tornado.options import options, define
import os

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
    tornado.options.parse_config_file(os.path.join(root, 'site.conf'))
    tornado.options.parse_command_line()
