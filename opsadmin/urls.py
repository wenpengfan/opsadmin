from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from opsadmin.views import index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^navi/', include('navi.urls')),
    url(r'^cmdb/', include('cmdb.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^config/', include('config.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^appconf/', include('appconf.urls')),
    url(r'^orders/', include('orders.urls')),
    url(r'^workload/', include('workload.urls')),
]
