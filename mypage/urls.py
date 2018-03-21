from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^preshot_routine/$', views.preshot_routine, name='mp_preshot_routine'),
    url(r'^diary/$', views.diary, name='mp_diary'),
    url(r'^goal_setting/$', views.goal_setting, name='mp_goal_setting'),
    url(r'^ltg_submit/$', views.ltg_submit, name='mp_ltg_submit'),
    url(r'^dg_submit/$', views.dg_submit, name='mp_dg_submit'),
    url(r'^ltg_date_exsist/(?P<date>\d+)/$', views.ltg_date_exsist),
    url(r'^ltg_date_exsist/$', views.ltg_date_exsist),
    url(r'^dg_exsist/(?P<date>\d+)/$', views.dg_date_exsist),
    url(r'^dg_exsist/$', views.dg_date_exsist),
    url(r'^diary_exsist/$', views.diary_exsist),
    url(r'^diary_exsist/(?P<date>\d+)/(?P<competition_level>\d+)/(?P<dumped_contents>\d+)/$', views.diary_exsist),
]
