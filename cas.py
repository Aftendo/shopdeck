from flask import Blueprint, request, render_template, make_response
import xmltodict, time, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopdeck.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from shopdeckdb.models import *
from django.core.exceptions import ObjectDoesNotExist

print("CAS Starting Up")

cas = Blueprint("cas", "cas")
@cas.route("/cas/services/CatalogingSOAP", methods=['POST'])
def soap():
    if request.get_data() == b"IwI":
        return "TwT"
    try:
        parsed = xmltodict.parse(request.get_data())
    except:
        return "Error"
    if request.headers.get('User-Agent') != "CTR EC 040600 Mar 14 2012 13:32:39":
        return "Error"
    if "cas:ListTitlesEx" in parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']:
        try:
            title = Title.objects.get(tid=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['cas:ListTitlesEx']['cas:TitleId'])
        except ObjectDoesNotExist:
            return "Error"
        r = make_response(render_template("cas/listTitlesEx.xml", id=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['cas:ListTitlesEx']['cas:DeviceId'], message=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['cas:ListTitlesEx']['cas:MessageId'],time=int(round(time.time()*1000)), t=title))
        r.headers.set("Content-Type", "text/xml; charset=utf-8")
        return r