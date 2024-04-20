from flask import Blueprint, send_from_directory
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopdeck.settings')
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
from shopdeckdb.models import *
from django.core.exceptions import ObjectDoesNotExist

assetcdn_directory = 'assetcdn'

print("Local CDN Starting Up")

cdn = Blueprint("web", __name__)

@cdn.route('/assets/<path:filename>')
def serve_file(filename):
    file_path = os.path.join(assetcdn_directory, filename)
    return send_from_directory(assetcdn_directory, filename) if os.path.isfile(file_path) else ("File not found", 404)
