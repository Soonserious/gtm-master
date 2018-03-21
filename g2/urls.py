from django.conf.urls import url
from . import views


urlpatterns = [
    # Evaluating
    url(r'^eval_golf_swing/$', views.eval_golf_swing, name='g2_eval_golf_swing'),
    url(r'^eval_short_game/$', views.eval_short_game, name='g2_eval_short_game'),
    url(r'^eval_putting/$', views.eval_putting, name='g2_eval_putting'),

    # Profile
    url(r'^profile/$', views.profile, name='g2_profile'),

    url(r'^update/$', views.update, name='g2_update'),
]
