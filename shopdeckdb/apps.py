from django.apps import AppConfig

print("Commonware initializing")

class ShopdeckdbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopdeckdb'
