import os

# Parse DEBUG from env. Accepts 'True'/'true'/'1' as truthy; defaults to False (production-safe).
_debug_env = os.environ.get('DEBUG', 'False')
DEBUG = _debug_env.lower() in ('1', 'true', 'yes')

if DEBUG:
    # Local development settings
    from .development import *  
else:
    # Production settings by default
    from .production import *  
