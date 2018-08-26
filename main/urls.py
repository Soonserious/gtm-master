from django.conf.urls import url
from . import views
from . import forms
import django.contrib.auth.views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signin/$', django.contrib.auth.views.login,
        {'template_name': 'registration/sign_in.html',
         'authentication_form': forms.SignInForm},
        name='sign_in'),
    url(r'^signout/$', django.contrib.auth.views.logout,
        {'next_page': '/'}, name='sign_out'),
    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'^account/$', views.account, name='account'),
    url(r'^aside/$',views.aside,name='aside'),
]
