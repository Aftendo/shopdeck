from flask import Blueprint, make_response, request
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopdeck.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from shopdeckdb.models import *
from django.core.exceptions import ObjectDoesNotExist
import os.path

print("CDN Services Starting Up")

ccs = Blueprint("ccs", "ccs")
@ccs.route("/ccs/download/<tid>/tmd.<version>", methods=['GET'])
def download_tmd(tid, version):
    try:
        title = Title.objects.get(tid=str(tid))
    except ObjectDoesNotExist:
        return "Error"
    try:
        ds = Client3DS.objects.get(consoleid=request.args.get('deviceId'))
    except ObjectDoesNotExist:
        return "Error"
    try:
        owned = ownedTitle.objects.get(title=title, owner=ds)
    except ObjectDoesNotExist:
        return "error"
    if owned.version < title.version:
        owned.version = title.version
        owned.save()
    path = str(os.path.dirname(__file__))+"/cdn/"+str(tid)+"/tmd.bin"
    if not os.path.isfile(path):
        return "error"
    f = open(path, mode="rb")
    r = make_response(f.read())
    r.headers.set("Content-Type", "application/octet-stream")
    return r
@ccs.route("/ccs/download/<tid>/<app>", methods=['GET'])
def download_app(tid, app):
    path = str(os.path.dirname(__file__))+"/cdn/"+str(tid)+"/"+str(app)+".app"
    if not os.path.isfile(path):
        return "error"
    f = open(path, mode="rb")
    r = make_response(f.read())
    r.headers.set("Content-Type", "application/octet-stream")
    return r