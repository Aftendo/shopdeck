from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.connect, name='login'),
    path('signup', views.register, name='register'),
    path('logout', views.disconnect, name="logout"),
    path('title/<int:tid>', views.title, name="title"),
    path('wishlist/add', views.add_wishlist, name="wishlist_add"),
    path('wishlist/remove', views.remove_wishlist, name="remove_wislist"),
    path('wishlist', views.wishlist, name="wishlist"),
    path('ecommerce/current', views.current_balance, name="current"),
    path('ecommerce/add', views.add_balance, name="add_balance"),
    path('downloaded', views.downloaded, name="downloaded"),
    path('search', views.search, name="search")
]