from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^shot_challenge/$', views.shot_challenge, name='g3_shot_challenge'),
    url(r'^short_game/$', views.short_game, name='g3_short_game'),
    url(r'^putting_game/$', views.putting_game, name='g3_putting_game'),
    url(r'^scoring_game/$', views.scoring_game, name='g3_scoring_game'),

    url(r'^tee_shot_submit/$', views.tee_shot_submit, name='g3_tee_shot_submit'),
    url(r'^approach_shot_submit/$', views.approach_shot_submit, name='g3_approach_shot_submit'),
    url(r'^fifty_four_shot_submit/$', views.fifty_four_shot_submit, name='g3_fifty_four_shot_submit'),

    url(r'^seve_game_submit/$', views.seve_game_submit, name='g3_seve_game_submit'),
    url(r'^nine_hole_submit/$', views.nine_hole_submit, name='g3_nine_hole_submit'),
    url(r'^hogan_game_submit/$', views.hogan_game_submit, name='g3_hogan_game_submit'),
    url(r'^scoring_game_submit/$', views.scoring_game_submit, name='g3_scoring_game_submit'),
    # Profile
    url(r'^profile/$', views.profile, name='g3_profile'),
    url(r'^update/$', views.update, name='g3_update'),
    url(r'^date_exsist/$', views.date_exsist),
]
