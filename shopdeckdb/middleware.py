from shopdeck import settings
from django.http import JsonResponse

class ShopMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if settings.IN_MAINTENANCE:
			return JsonResponse({"error": {"code": "6516", "message": "Maintenance is in progress.\nPlease come back later."}}, status=400)
		response = self.get_response(request)
		return response