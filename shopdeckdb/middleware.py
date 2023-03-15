'''
General purpose Middleware for both the eShop & Web UI servers
'''
from shopdeck import settings
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

class ShopMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if settings.IN_MAINTENANCE:
			if request.path.startswith("/ninja/ws") or request.path.startswith("/samurai/ws"):
				return JsonResponse({"error": {"code": "6516", "message": "Maintenance is in progress.\nPlease come back later."}}, status=400)
			else:
				return HttpResponse("Maintenance is in progress. Please come back later.", status=503)
		if not request.path.startswith("/admin") and request.user.is_authenticated and request.user.linked_ds == None:
			return HttpResponse("Your account is misconfigured. Contact an admin. It is not currently usable.")
		if request.user.is_authenticated and request.user.linked_ds != None:
			if request.user.linked_ds.is_terminated:
				return HttpResponse("Your account has been terminated.")
		if not request.user.is_authenticated and not request.path.startswith("/ninja") and not request.path.startswith("/samurai") and not request.path.startswith("/login") and not request.path.startswith("/signup") and not request.path == "/":
			return HttpResponseRedirect("/")
		response = self.get_response(request)
		return response