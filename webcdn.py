from flask import Blueprint, send_from_directory
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopdeck.settings')
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
from shopdeckdb.models import *
from django.core.exceptions import ObjectDoesNotExist

webcdn_directory = 'webcdn'

print("CDN (for images, etc.) Services Starting Up")

ccs = Blueprint("web", __name__)

@ccs.route('/webcdn/<path:filename>')
def serve_file(filename):
    file_path = os.path.join(webcdn_directory, filename)
    return send_from_directory(webcdn_directory, filename) if os.path.isfile(file_path) else ("File not found", 404)
