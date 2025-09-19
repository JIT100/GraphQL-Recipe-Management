import os

# you need to set DEBUG = TRUE or False depending on the enviroment. Debug False is for production & True is for Local.

DEBUG = os.environ.get('DEBUG', 'True') == 'True'
if DEBUG:
    from .development import *  # noqa
else:
    pass
