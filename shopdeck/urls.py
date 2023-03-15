"""shopdeck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

handler404 = 'webui.views.err404'
handler500 = 'webui.views.err500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webui.urls')),
    path('ninja/ws/', include('api.urls')),
    path('samurai/ws/<str:region>/', include('metadata.urls')),
]
