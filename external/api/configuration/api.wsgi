#/var/www/api/api.wsgi
import sys

sys.path.append("/var/www/api")

from api import app as application