from flask import Blueprint, request, render_template, make_response
import xmltodict, time, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopdeck.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from shopdeckdb.models import *
from django.core.exceptions import ObjectDoesNotExist

print("IAS Starting Up")

ias = Blueprint("ias", "ias")
@ias.route("/ias/services/IdentityAuthenticationSOAP", methods=['POST'])
def soap():
    if request.get_data() == b"UwU":
        return "OwO"
    try:
        parsed = xmltodict.parse(request.get_data())
    except:
        return "Error"
    if request.headers.get('User-Agent') != "CTR EC 040600 Mar 14 2012 13:32:39":
        return "Error"
    if 'ias:SetIVSData' in parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']:
        try:
            ds = Client3DS.objects.get(consoleid=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:SetIVSData']['ias:DeviceId'])
        except ObjectDoesNotExist:
            return "Error"
        r = make_response(render_template("ias/setIVSData.xml", id=ds.consoleid, message=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:SetIVSData']['ias:MessageId'],time=int(round(time.time()*1000)), iasname="SetIVSDataResponse"))
        r.headers.set("Content-Type", "text/xml; charset=utf-8")
        return r
    if 'ias:SetCountry' in parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']:
        try:
            ds = Client3DS.objects.get(consoleid=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:SetCountry']['ias:DeviceId'])
        except ObjectDoesNotExist:
            return "Error"
        r = make_response(render_template("ias/setIVSData.xml", id=ds.consoleid, message=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:SetCountry']['ias:MessageId'],time=int(round(time.time()*1000)), iasname="SetCountryResponse"))
        r.headers.set("Content-Type", "text/xml; charset=utf-8")
        return r
    if 'ias:GetChallenge' in parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']:
        try:
            ds = Client3DS.objects.get(consoleid=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:GetChallenge']['ias:DeviceId'])
        except ObjectDoesNotExist:
            return "Error"
        r = make_response(render_template("ias/getChallenge.xml", id=ds.consoleid, message=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:GetChallenge']['ias:MessageId'],time=int(round(time.time()*1000))))
        r.headers.set("Content-Type", "text/xml; charset=utf-8")
        return r
    if 'ias:Register' in parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']:
        if str(parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:Register']['ias:Challenge']) != '526726942':
            return "Error"
        try:
            ds = Client3DS.objects.get(consoleid=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:Register']['ias:DeviceId'])
        except ObjectDoesNotExist:
            return "Error"
        r = make_response(render_template("ias/register.xml", id=ds.consoleid, message=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:Register']['ias:MessageId'],time=int(round(time.time()*1000)), accountid=ds.id, devicetoken=ds.devicetoken, country=ds.country))
        r.headers.set("Content-Type", "text/xml; charset=utf-8")
        return r
    if 'ias:Unregister' in parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']:
        try:
            ds = Client3DS.objects.get(consoleid=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:Unregister']['ias:DeviceId'])
        except ObjectDoesNotExist:
            return "Error"
        if int(parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:Unregister']['ias:AccountId']) != int(ds.id):
            return "Error"
        ds.delete()
        r = make_response(render_template("ias/unregister.xml", id=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:Unregister']['ias:DeviceId'], message=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:Unregister']['ias:MessageId'],time=int(round(time.time()*1000))))
        r.headers.set("Content-Type", "text/xml; charset=utf-8")
        return r
    if 'ias:GetRegistrationInfo' in parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']:
        if str(parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:GetRegistrationInfo']['ias:Challenge']) != '526726942':
            return "Error"
        try:
            ds = Client3DS.objects.get(consoleid=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:GetRegistrationInfo']['ias:DeviceId'])
        except ObjectDoesNotExist:
            return "Error"
        r = make_response(render_template("ias/getRegistrationInfo.xml", id=ds.consoleid, message=parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ias:GetRegistrationInfo']['ias:MessageId'],time=int(round(time.time()*1000)), accountid=ds.id, devicetoken=ds.devicetoken, country=ds.country))
        r.headers.set("Content-Type", "text/xml; charset=utf-8")
        return r