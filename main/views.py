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
        user_form = forms.SignUpUserForm(data=request.POST)
        member_form = forms.SignUpMemberForm(data=request.POST)
        if user_form.is_valid() and member_form.is_valid():
            user = user_form.save()
            member = member_form.save(commit=False)
            member.user = user
            member.save()
            return redirect('home')
        else:
            errors = dict()
            for e_dict in [user_form.errors, member_form.errors]:
                errors.update(e_dict)
            print('signup error: {}'.format(errors))
            first_error_key = list(errors.keys())[0]
            error_messeage = '{}: {}'.format(first_error_key, errors[first_error_key][0])
            context = {
                'error_occurred': True,
                'error': error_messeage,
            }
            return render(request, 'registration/sign_up.html', context=context)
    # GET
    else:
        return render(request, 'registration/sign_up.html')


def account(request):
    if request.method == 'GET':
        return render(request, 'registration/account.html')

    elif request.method == 'POST':
        print(request.POST)
        context = {'error': 0}
        user = User.objects.get(username=request.user.username)
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
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        context['user'] = user
        context['error'] = False
        context['message'] = 'Your account information had been changed.'

        return render(request, 'registration/account.html', context=context)


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
