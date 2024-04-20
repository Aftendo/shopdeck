from flask import Blueprint, make_response, request
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopdeck.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from shopdeckdb.models import *
from django.core.exceptions import ObjectDoesNotExist
import os.path
webcdn_directory = '/webcdn/'

ccs = Blueprint("web", "web")

@wcss.route('/webcdn/<path:filename>')
def serve_file(filename):
    file_path = os.path.join(webcdn_directory, filename)
    if os.path.isfile(file_path):
        return send_from_directory(webcdn_directory, filename)
    else:
        return "File not found", 404

@app.route('/')
def home():
    return 'CDN (for images .etc) Services Starting Up'

if __name__ == '__main__':
    app.run()
