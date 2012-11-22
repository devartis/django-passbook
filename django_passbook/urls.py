from django.conf.urls import patterns, url
from django_passbook.views import register_pass

urlpatterns = patterns('',
    url(r'^v1/devices/(?P<device_library_id>.+)/registrations/(?P<pass_type_id>[\w\.\d]+)/(?P<serial_number>.+)$', register_pass),
)
