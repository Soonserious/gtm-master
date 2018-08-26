# -*- coding: utf-8 -*-
from functools import wraps

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms import modelformset_factory
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.utils.decorators import available_attrs
from django.views.decorators.csrf import csrf_exempt
import json

from . import forms
from . import models


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            full_name = None
        else:
            full_name = models.Member.objects.get(user=request.user).full_name
    else:
        full_name = None
    return render(request, 'index.html', context={'full_name': full_name})


@csrf_exempt
def manager(request):
    return render(request, reverse('admin:main_member_changelist'))


def sign_up(request):
    # POST
    if request.method == 'POST':
        print(request.POST)
        user_form = forms.SignUpUserForm(data=request.POST)
        member_form = forms.SignUpMemberForm(data=request.POST)
        if user_form.is_valid() and member_form.is_valid():
            user = user_form.save()
            member = member_form.save(commit=False)
            member.user = user
            member.save()
            context={'success':'회원가입을 축하합니다'}
            return HttpResponse(json.dumps(context),content_type="application/json");
            # return render(request, 'index.html', context={'alertSignup': True})
            # return redirect('home')
        else:
            errors = dict()
            for e_dict in [user_form.errors, member_form.errors]:
                errors.update(e_dict)
            print('signup error: {}'.format(errors))
            first_error_key = list(errors.keys())[0]
            error_messeage = '{}: {}'.format(first_error_key, errors[first_error_key][0])
            context = {
                'error_occurred': True,
                'error': error_messeage
            }
            return HttpResponse(json.dumps(context),content_type="application/json");
            # return render(request, 'registration/sign_up.html', context=context)
    # GET
    else:
        return render(request, 'registration/sign_up.html')

def account(request):
    if request.method == 'GET':
        member=models.Member.objects.get(user=request.user)
        ret={}
        ret['username']=request.user.username
        ret['sex']=member.sex
        ret['association']=member.association
        ret['full_name']=member.full_name
        ret['phone_number']=member.phone_number
        ret['email']=member.email
        ret['birth']=member.birth
        return render(request, 'registration/account.html',ret)
    elif request.method == 'POST':
        context = {'error': 0}
        print(request.POST)
        user = User.objects.get(username=request.user.username)
        member=models.Member.objects.get(user=request.user)
        if 'current_pw' in request.POST:
            if not request.user.check_password(request.POST['current_pw']):
                context['error'] = True
                context['message'] = 'Current password is not correct.'
                render(request, 'registration/account.html', context=context)
            elif request.POST['new_pw_1'] != request.POST['new_pw_2']:
                context['error'] = True
                context['message'] = 'New passwords do not match.'
                render(request, 'registration/account.html', context=context)
            else:
                user.set_password(request.POST['new_pw_1'])
                context['error'] = False
        member_form = forms.SignUpMemberForm(data=request.POST)
        try:

            if member_form.is_valid():
                member.birth=member_form.cleaned_data['birth']
                member.email=member_form.cleaned_data['email']
                member.phone_number=member_form.cleaned_data['phone_number']
                member.association = member_form.cleaned_data['association']
                member.sex = member_form.cleaned_data['sex']
                member.save()
            else:
                errors = dict()
                for e_dict in [member_form.errors]:
                    errors.update(e_dict)
                first_error_key = list(errors.keys())[0]
                error_message = '{}: {}'.format(first_error_key, errors[first_error_key][0])
                context['error'] = True
                context['message']=error_message
                return render(request, 'registration/account.html', context=context)
            context['username'] = member.user.username
            context['sex'] = member.sex
            context['association'] = member.association
            context['full_name'] = member.full_name
            context['phone_number'] = member.phone_number
            context['email'] = member.email
            context['birth'] = member.birth
            context['user'] = user
            context['error'] = False
            context['message'] = 'Your account information had been changed.'
            return render(request, 'registration/account.html', context=context)
        except Exception as ex:
            print(ex)
        # user.save()

def aside(request):
    return render(request,'common/aside.html',context={'next':request.GET["next"]})

def user_passes_test(test_func, message):
    """
    Decorator for views that checks that the user passes the given test,
    setting a message in case of no success. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if not test_func(request.user):
                messages.error(request, message)
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def has_permission_g1(user):
    if user.is_staff:
        return True
    else:
        member = models.Member.objects.get(user=user)
        return member.permission_g1


def has_permission_g2(user):
    if user.is_staff:
        return True
    else:
        member = models.Member.objects.get(user=user)
        return member.permission_g2


def has_permission_g3(user):
    if user.is_staff:
        return True
    else:
        member = models.Member.objects.get(user=user)
        return member.permission_g3


def has_permission_g4(user):
    if user.is_staff:
        return True
    else:
        member = models.Member.objects.get(user=user)
        return member.permission_g4


def has_permission_mypage(user):
    if user.is_staff:
        return True
    else:
        member = models.Member.objects.get(user=user)
        return member.permission_mypage
