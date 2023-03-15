#CRAPPY CODE WARNING(!)
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from shopdeck import settings
from shopdeckdb.models import *
from django.core.exceptions import ObjectDoesNotExist
import time, random, string

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@csrf_exempt
def service_hosts(request):
   res = {"services":{"service":[{"name":"CCIF","origin_fqdn":settings.SOAP_URL},{"name":"SAMURAI_CTR","origin_fqdn":settings.METADATA_API_URL,"cdn_fqdn":settings.METADATA_API_URL},{"name":"EOU","origin_fqdn":settings.SOAP_URL,"cdn_fqdn":settings.SOAP_URL}]}}
   return JsonResponse(res)

@csrf_exempt
def country(request, country):
   res = {"country_detail":{"region_code":"LOL","max_cash":{"amount":"99999,00 Credit","currency":"CREDIT","raw_value":"99999"},"loyalty_system_available":False,"legal_payment_message_required":False,"legal_business_message_required":False,"tax_excluded_country":False,"tax_free_country":False,"prepaid_card_available":True,"credit_card_available":False,"credit_card_store_available":False,"jcb_security_code_available":False,"nfc_available":False,"coupon_available":False,"my_coupon_available":True,"price_format":{"positive_prefix":"","positive_suffix":" Credit","negative_prefix":"- ","negative_suffix":" Credit","formats":{"format":[{"value":"# ### ### ###,##","digit":"#"}],"pattern_id":"5"}},"default_timezone":"+00:00","eshop_available":True,"name":country,"iso_code":country,"default_language_code":"en","language_selectable":False}}
   return JsonResponse(res)

@csrf_exempt
def open(request):
   data = request.POST
   if data.get("device_id")==None:
      return JsonResponse({"error": True})
   try:
      ds = Client3DS.objects.get(consoleid=data.get("device_id"))
   except ObjectDoesNotExist:
      return JsonResponse({"error": True})
   if ds.is_terminated:
      return JsonResponse({"error": {"code": "8008", "message": "Your account has been terminated. Sorry."}}, status=400)
   request.session['deviceid'] = data.get("device_id")
   currenttime = int(round(time.time()*1000))
   id = id_generator()
   res = {"session_config":{"country":ds.country,"saved_lang":ds.language,"shop_account_initialized":False,"device_link_updated":False,"owned_titles_modified":currenttime,"shared_titles_last_modified":currenttime,"server_time":currenttime,"devices":{"device":[{"name":"CTR","id":4}]},"auto_billing_contracted":False,"id":id}}
   return JsonResponse(res)

@csrf_exempt
def close(request):
   request.session.flush()
   return HttpResponse()

@csrf_exempt
def balance(request):
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   res = {"balance":{"amount":str(ds.balance)+",00 Credit","currency":"EUR","raw_value":str(ds.balance)}}
   return JsonResponse(res)

#This is due to how eShop servers handle my/wishlist/notice: its a empty json, even if you have wishlisted titles
@csrf_exempt
def dummy_wishlist(request):
   res = {"wishlist_notice":{"wished_title_id":[],"total":0}}
   return JsonResponse(res)

@csrf_exempt
def wishlist(request):
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   wishlisted_titles = wishlistedTitle.objects.filter(owner=ds)
   wishlisted = []
   for title in wishlisted_titles:
      wishlisted.append({"platform": {"name": title.title.platform.name, "id": title.title.platform.id, "device": "CTR", "category": title.title.genre.id}, "publisher": {"name": title.title.publisher.publisher_name, "id": title.title.publisher.id}, "display_genre": title.title.genre.name, "release_date_on_eshop": str(title.title.date), "release_date_on_original": str(title.title.date), "retail_sales": False, "eshop_sales": True, "in_app_purchase": title.title.in_app_purchase, "name": title.title.name, "id": title.title.id, "icon_url": title.title.icon_url, "banner_url": title.title.banner_url})
   res = {"wishlist":{"wished_title":wishlisted,"total":len(wishlisted)}}
   return JsonResponse(res)

#FIXME: Make this not just a static JSON response.
@csrf_exempt
def owned_coupons(request):
   res = {"coupons":{}}
   return JsonResponse(res)

@csrf_exempt
def ownedtitles(request):
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   owned_titles = ownedTitle.objects.filter(owner=ds)
   owned = []
   i = 0
   for title in owned_titles:
      owned.append({"title_id": title.title.tid, "id": title.title.id, "index": i})
      i+1

   res = {"owned_titles":{"owned_title":owned}}
   return JsonResponse(res)

@csrf_exempt
def language(request):
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   res = {"session_config":{"saved_lang":ds.language}}
   return JsonResponse(res)

@csrf_exempt
def empty(request):
   return JsonResponse({})

@csrf_exempt
def online_price(request, country):
   if request.GET.get('title[]') == None:
      return JsonResponse({"error": True})
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   tlist = list(request.GET.get('title[]').split(","))
   titles = []
   for ind_title in tlist:
      try:
         title = Title.objects.get(id=int(ind_title))
         try:
            titleowned = ownedTitle.objects.get(title=title, owner=ds)
            is_title_owned = True
         except ObjectDoesNotExist:
            is_title_owned = False
         if title.price == 0:
            titleprice = "Free"
         else:
            titleprice = str(title.price)+" Credit"
         titles.append({"title_id": int(ind_title), "eshop_sales_status": "onsale", "price": {"regular_price": {"amount": titleprice, "currency": "CREDIT", "raw_value": str(title.price), "id": 2172116800}}, "title_owned": is_title_owned})
      except ObjectDoesNotExist:
         return JsonResponse({"error": True})
   res = {"online_prices": {"online_price": titles}}
   return JsonResponse(res)

@csrf_exempt
def ec_info(request, country, tid):
   try:
      title = Title.objects.get(id=tid)
   except:
      return JsonResponse({"error": True})
   res = {"title_ec_info":{"title_id":title.tid,"content_size":title.size,"title_version":title.version,"disable_download":title.is_not_downloadable}}
   return JsonResponse(res)

@csrf_exempt
def put_wishlist(request):
   try:
      title = Title.objects.get(id=int(request.POST.get("id")))
   except:
      return JsonResponse({"error": True})
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   try:
      wishlisted = wishlistedTitle.objects.get(title=title, owner=ds)
      return JsonResponse({"error": True})
   except ObjectDoesNotExist:
      pass
   wishlisted = wishlistedTitle.objects.create(title=title, owner=ds)
   wishlisted.save()
   return JsonResponse({})

@csrf_exempt
def delete_wishlist(request, tid):
   try:
      title = Title.objects.get(id=int(tid))
   except:
      return JsonResponse({"error": True})
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   try:
      wishlisted = wishlistedTitle.objects.get(title=title, owner=ds)
   except ObjectDoesNotExist:
      return JsonResponse({"error": True})
   wishlisted.delete()
   return JsonResponse({})

@csrf_exempt
def check_redeemable(request):
   try:
      card = redeemableCard.objects.get(code=request.POST.get("card_number"))
   except:
      return JsonResponse({"error": {"code": "6561", "message": "This code is incorrect.\nPlease check up your code and try again."}}, status=400)
   if card.used:
      return JsonResponse({"error": {"code": "3101", "message": "This code is already used.\nSorry!"}}, status=400)
   if card.is_money:
      res = {"redeemable_card": {"number": request.POST.get("card_number"),"cash": {"amount": card.content+" Credit","currency": "CREDIT","raw_value": card.content}}}
      return JsonResponse(res)
   else:
      try:
         title = Title.objects.get(tid=card.content)
      except ObjectDoesNotExist:
         return JsonResponse({"error": {"code": "5615", "message": "The corresponding title was not found.\nContact an administrator."}}, status=400)
      if request.POST.get("tin") != None:
         return JsonResponse({"error": {"code": "6969", "message": "This is a title download code.\nPlease use the right tool."}})
      res = {"redeemable_card": {"number": request.POST.get("card_number"), "contents": {"content": [{"title": {"name": title.name, "id": title.id}}]},"title_ec_info": {"title_id": title.tid, "content_size": title.size, "title_version": title.version}}}
      return JsonResponse(res)
   
@csrf_exempt
def pretransac_redeem(request):
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   res = {"prereplenish_info": {"current_balance": {"amount": str(ds.balance)+" Credit", "currency": "CREDIT", "raw_value": str(ds.balance)},"replenish_amount": {"amount": str(request.GET.get("replenish_amount"))+" Credit", "currency": "CREDIT", "raw_value": str(request.GET.get("replenish_amount"))},"post_balance": {"amount": str(int(float(request.GET.get("replenish_amount")))+ds.balance)+" Credit", "currency": "CREDIT", "raw_value": str(int(float(request.GET.get("replenish_amount")))+ds.balance)}}}
   return JsonResponse(res)

@csrf_exempt
def add_money_prepaid(request):
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   try:
      card = redeemableCard.objects.get(code=request.POST.get("card_number"))
   except:
      return JsonResponse({"error": {"code": "6561", "message": "This code is incorrect.\nPlease check up your code and try again."}}, status=400)
   if card.used:
      res = {"error": {"code": "4626", "message": "This code is already used.\nSorry!"}}
      return JsonResponse(res, status=400)
   res = {"transaction_result": {"transaction_id": 1,"post_balance": {"amount": str(int(card.content)+ds.balance)+" Credit","currency": "CREDIT","raw_value": str(int(card.content)+ds.balance)},"integrated_account": True}}
   card.used = True
   card.save()
   ds.balance = int(card.content)+ds.balance
   ds.save()
   return JsonResponse(res)

@csrf_exempt
def prepurchase_info(request, country, tid):
   try:
      title = Title.objects.get(id=int(tid))
   except:
      return JsonResponse({"error": True})
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   res = {"prepurchase_info":{"tax_excluded":False,"purchasing_content":[{"eshop_sales_status":"onsale","content_size":title.size,"payment_amount":{"price":{"regular_price":{"amount":str(title.price)+",00 Credit","currency":"CREDIT","raw_value":str(title.price),"id":2172116800}},"total_amount":{"amount":str(title.price)+",00 Credit","currency":"CREDIT","raw_value":str(title.price)}}}],"current_balance":{"amount":str(ds.balance)+",00 Credit","currency":"CREDIT","raw_value":str(ds.balance)},"post_balance":{"amount":str(ds.balance-title.price)+",00 Credit","currency":"EUR","raw_value":str(ds.balance-title.price)},"total_amount":{"price":{"regular_price":{"amount":str(title.price)+",00 Credit","currency":"CREDIT","raw_value":str(title.price)}},"total_amount":{"amount":str(title.price)+",00 Credit","currency":"CREDIT","raw_value":str(title.price)}}}}
   return JsonResponse(res)

@csrf_exempt
def purcahse_title(request, country, tid):
   try:
      title = Title.objects.get(id=int(tid))
   except:
      return JsonResponse({"error": True})
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   if not title.public:
      return JsonResponse({"error": {"code": "6265", "message": "This title is not public.\nYou cannot download it."}}, status=400)
   if ds.balance - title.price < 0:
      return JsonResponse({"error": {"code": "8167", "message": "You don't have enough money for that."}})
   try:
      owned = ownedTitle.objects.get(title=title, owner=ds)
   except ObjectDoesNotExist:
      ds.balance = ds.balance - title.price
      ds.save()
      owned = ownedTitle.objects.create(title=title, version=title.version, owner=ds)
      owned.save()
   res = {"transaction_result":{"transaction_id":1,"title_id":title.tid,"ticket_id":int(title.ticket_id),"post_balance":{"amount":str(ds.balance)+",00 Credit","currency":"CREDIT","raw_value":str(ds.balance)},"business_type":"NCL_DIST","integrated_account":True}}
   return JsonResponse(res)

@csrf_exempt
def tax_location(request):
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   res = {"tax_location": {"state": "uwuland", "state_code": ds.country, "id": 71647}}
   return JsonResponse(res)

@csrf_exempt
def redeem_title(request, country, tid):
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   try:
      title = Title.objects.get(id=int(tid))
   except:
      return JsonResponse({"error": True})
   try:
      card = redeemableCard.objects.get(code=request.POST.get("card_number"))
   except:
      return JsonResponse({"error": {"code": "6561", "message": "This code is incorrect.\nPlease check up your code and try again."}})
   if card.content != title.tid:
      return JsonResponse({"error": {"code": "9468", "message": "Invalid title ID.\nPlease check up your code and try again."}}, status=400)
   card.used = True
   card.save()
   owned = ownedTitle.objects.create(title=title, version=title.version, owner=ds)
   owned.save()
   res = {"transaction_result":{"transaction_id":1,"title_id":title.tid,"ticket_id":int(title.ticket_id),"post_balance":{"amount":str(ds.balance)+",00 Credit","currency":"CREDIT","raw_value":str(ds.balance)},"business_type":"NCL_DIST","integrated_account":True}}
   return JsonResponse(res)
   
@csrf_exempt
def transactions(request):
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   return JsonResponse({"error": {"code": "8458", "message": "Hello!\nHere is your 3DS Key:\n"+ds.uniquekey}}, status=400)

@csrf_exempt
def shared_titles(request):
   try:
      ds = Client3DS.objects.get(consoleid=request.session["deviceid"])
   except:
      return JsonResponse({"error": True})
   ownedtitles = ownedTitle.objects.filter(owner=ds)
   wishlisted = []
   for title in ownedtitles:
      wishlisted.append({"platform": {"name": title.title.platform.name, "id": title.title.platform.id, "device": "CTR", "category": title.title.genre.id}, "publisher": {"name": title.title.publisher.publisher_name, "id": title.title.publisher.id}, "display_genre": title.title.genre.name, "release_date_on_eshop": str(title.title.date), "release_date_on_original": str(title.title.date), "retail_sales": False, "eshop_sales": True, "in_app_purchase": title.title.in_app_purchase, "name": title.title.name, "id": title.title.id, "icon_url": title.title.icon_url, "banner_url": title.title.banner_url})
   res = {"owned_titles":{"owned_title":wishlisted,"total":len(wishlisted)}}
   return JsonResponse(res)

@csrf_exempt
def id_pair(request):
   return JsonResponse({"error": {"code": "6569", "message": "Due to technical limitations,\nthis functionnality is not available."}}, status=401)

@csrf_exempt
def public_status(request, country):
   if request.GET.get("ns_uid") == None:
      return JsonResponse({"error": True})
   try:
      title = Title.objects.get(id=int(request.GET.get("ns_uid")))
   except:
      return JsonResponse({"error": {"code": "5546", "message": "Title not found."}}, status=400)
   if title.public:
      type = "PUBLIC"
   else:
      type = "PRIVATE"
   res = {"title_public_status":{"public_status":type,"type":"T","ns_uid":title.id,"title_id":title.tid}}
   return JsonResponse(res)

@csrf_exempt
def votable_titles(request):
    return JsonResponse({"error": {"code": "5626", "message": "WIP. Not ready yet."}}, status=400)

@csrf_exempt
def votes(request):
    return JsonResponse({"error": {"code": "5626", "message": "WIP. Not ready yet."}}, status=400)
