from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from fitness import views
import os

rtr = routers.DefaultRouter()
rtr.register(r'k', views.KVS, basename='k')
rtr.register(r'g', views.GVS, basename='g')
rtr.register(r'd', views.DVS, basename='d')
rtr.register(r'p', views.PVS, basename='p')

cs = os.environ.get('CODESPACE_NAME')
if cs:
    bu = f"https://{cs}-8000.app.github.dev"
else:
    bu = "http://localhost:8000"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hub/', views.hub, name='hub'),
    path('hub/', include(rtr.urls)),
    path('hub/rank/', views.rank, name='rank'),
    path('hub/bat/', views.bat, name='bat'),
]
