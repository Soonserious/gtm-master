from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^ocean_test/$', views.ocean_test, name='g4_ocean_test'),
    url(r'^ocean_test_submit/$', views.ocean_test_submit, name='g4_ocean_test_submit'),
    url(r'^gmet/$', views.gmet, name='g4_gmet'),
    url(r'^gmet_submit/$', views.gmet_submit, name='g4_gmet_submit'),
    url(r'^tops/$', views.tops, name='g4_tops'),
    url(r'^tops_submit/$', views.tops_submit, name='g4_tops_submit'),
    url(r'^fss/$', views.fss, name='g4_fss'),
    url(r'^fss_submit/$', views.fss_submit, name='g4_fss_submit'),
    url(r'^acsi/$', views.acsi, name='g4_acsi'),
    url(r'^acsi_submit/$', views.acsi_submit, name='g4_acsi_submit'),
    url(r'^course_management/$', views.course_management, name='g4_course_management'),
    url(r'^course_management_submit/$', views.course_management_submit, name='g4_course_management_submit'),
    url(r'^profile/$', views.profile, name='g4_profile'),
    url(r'^update/$', views.update, name='g4_update'),
]
