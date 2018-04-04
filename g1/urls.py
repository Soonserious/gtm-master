from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^round/$', views.round, name='g1_round'),
    url(r'^round_result/$', views.round_result, name='g1_round_result'),
    url(r'^round_result_add/$', views.round_result_add, name='g1_round_result_add'),
    url(r'^round_result_add_submit/$', views.round_result_add_submit, name='g1_round_result_add_submit'),
    url(r'^field_info/$', views.field_info, name='g1_field_info'),   # for name only.
    url(r'^field_info/(?P<field_name>\d+)/$', views.field_info),
    url(r'^field_add/$', views.field_add, name='g1_field_add'),
    url(r'^course_info$', views.course_info, name='g1_course_info'),    # for name only.
    url(r'^course_info/(?P<field_id>\d+)/(?P<tee_type>\d+)/$', views.course_info),
    url(r'^course_add$', views.course_add, name='g1_course_add'),   # for name only.
    url(r'^course_add/(?P<field_id>\d+)/(?P<tee_type>\d+)/$', views.course_add),
    url(r'^criteria/$', views.criteria, name='g1_criteria'),
    url(r'^profile$', views.profile, name='g1_profile'),
    url(r'^update$', views.update, name='g1_update'),
    url(r'^field_remove$',views.field_remove, name='g1_field_remove'),
    url(r'^field_remove$',views.field_remove, name='g1_field_remove'),
    url(r'^view_course/(?P<course_id>\d+)/$', views.view_course, name='g1_view_course'),
    url(r'^view_course/(?P<field_id>\d+)/$', views.view_course, name='g1_view_course'),
    url(r'^course_remove/(?P<course_id>\d+)/$', views.course_remove),
    url(r'^course_remove/$', views.course_remove),
    url(r'^remove_filed_and_course/$',views.remove_filed_and_course),
    url(r'^remove_filed_and_course/(?P<field_id>\d+)/$', views.remove_filed_and_course),
    url(r'^AVG_bride/$', views.AVG_bride),
    url(r'^play_rythm/$',views.play_rythm),
    url(r'^play_rythm/(?P<target_user_id>\d+)/$',views.play_rythm),
    url(r'^AVG_Stroke/$',views.AVG_Stroke),
    url(r'^administrator_par_input/$',views.administrator_par_input),
]
