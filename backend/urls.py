from django.urls import path, re_path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from network import views as network

urlpatterns = [
    path('', network.index),
    path('admin/', admin.site.urls),
    re_path(r'^search/(?P<query>.*)$', network.index),
    re_path(r'^node/(?P<nodeid>.*)$', network.node_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
