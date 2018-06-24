#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from main.views import user_passes_test, has_permission_mypage
from .models import PreshotRoutine, Diary, LongTermGoals, DailyGoals
from .forms import PreshotRoutineForm, DiaryForm, LongTermGoalsForm, DailyGoalsForm
import json
import re
from django.core.exceptions import ObjectDoesNotExist

def extract_comments_from_post(post):
    strategies_re = re.compile(r'^comment_(?P<i_idx>[0-9]+)_(?P<j_idx>[0-9]+)$')
    strategies = dict()
    for key, value in post.items():
        re_result = strategies_re.match(key)
        if re_result is None:
            continue
        # i_idx, j_idx: currently not used
        # i_idx = int(re_result.group('i_idx'))
        # j_idx = int(re_result.group('j_idx'))
        strategies[key] = value
    return strategies


def extract_contents_from_post(post):
    contents_re = re.compile(r'^content_(?P<i_idx>[0-9]+)$')
    contents = dict()
    for key, value in post.items():
        re_result = contents_re.match(key)
        if re_result is None:
            continue
        contents[key] = value
    return contents


@login_required
@user_passes_test(has_permission_mypage, "My Page 이용 권한이 없습니다.")
def preshot_routine(request):
    if request.method == 'GET':
        context = dict()
        queried = PreshotRoutine.objects.filter(user=request.user).order_by('-update_time')
        if queried.exists():
            context['record_exists'] = True
            model = queried[0]
            strategies = json.loads(model.dumped_strategies)
            context.update(strategies)
        else:
            context['record_exists'] = False
        return render(request, 'mypage/preshot_routine.html', context=context)
    else:
        form = PreshotRoutineForm(request.POST)
        if not form.is_valid():
            return HttpResponse(form.errors)
        model = form.save(commit=False)
        model.user = request.user
        strategies = extract_comments_from_post(request.POST)
        model.dumped_strategies = json.dumps(strategies)
        model.save()
        return JsonResponse({'status': 'success'})


@login_required
@user_passes_test(has_permission_mypage, "My Page 이용 권한이 없습니다.")
def diary(request):
    try :
        if request.method == 'GET':
            context = dict()
            queried = Diary.objects.filter(user=request.user).order_by('-update_time')
            if queried.exists():
                context['record_exists'] = 1
                model = queried[0]
                contents = json.loads(model.dumped_contents)
                context.update(contents)
                context['date'] = model.date.isoformat()
                context['competition_level'] = model.competition_level
                context['competition_name'] = model.competition_name

            else:
                context['record_exists'] = 0
            return render(request, 'mypage/diary.html', context=context)
        else:
            model = None
            competition_level = int(request.POST['competition_level'])
            form = DiaryForm(request.POST)
            try:
                model = Diary.objects.get(user=request.user, date = request.POST["date"],competition_level=request.POST["competition_level"])
            except ObjectDoesNotExist:
                model = Diary()
                if not form.is_valid():
                    return HttpResponse(form.errors)
                model.user = request.user
                model.competition_level = competition_level

                model.date = request.POST["date"]
            model.competition_name = request.POST["competition_name"]
            contents = extract_contents_from_post(request.POST)
            model.dumped_contents = json.dumps(contents)
            model.save()
            return JsonResponse({'status': 'success'})

    except Exception as ex:
        print(ex)

@login_required
@user_passes_test(has_permission_mypage, "My Page 이용 권한이 없습니다.")
def goal_setting(request):
    try:
        if request.method == 'GET':
            context = {}

            queried = LongTermGoals.objects.filter(user=request.user).order_by('-update_time')
            if queried.exists():
                model = queried[0]
                context["ltg_goal"] = json.loads(model.dumped_contents)

            queried = DailyGoals.objects.filter(user=request.user).order_by('-update_time')
            if queried.exists():
                dg_data = []
                i = 1
                for query in queried.iterator():
                    if i == 11:
                        break;
                    dumped_contents = json.loads(query.dumped_contents)

                    dg_data.append([i,
                                    dumped_contents['dg_date'.format(i)],
                                    dumped_contents['dg_content'.format(i)],
                                    dumped_contents['dg_achieved'.format(i)]])
                    i += 1
            else:
                dg_data = list(zip(list(range(10)), [''] * 10, [''] * 10, [False] * 10))
            context['dg_data'] = dg_data
            print(dg_data)
            return render(request, 'mypage/goal_setting.html', context=context)
        else:
            pass
    except Exception as ex :
        print(ex)

def ltg_submit(request):
    try:
        if request.method == 'GET':
            return
        dumped_contents = request.POST['contents']
        model = None
        try:
            model = LongTermGoals.objects.get(user=request.user, update_time=request.POST["ltg_date"])
        except ObjectDoesNotExist:
            model = LongTermGoals()
        model.update_time = request.POST["ltg_date"]
        print(model)
        model.user = request.user
        model.dumped_contents = dumped_contents

        model.save()
        return JsonResponse({'status': '목표 설정 및 성취 평가 저장 완료'})
    except Exception as ex:
        print(ex)

def dg_submit(request):
    try:
        if request.method == 'GET':
            return
        dumped_contents = request.POST['contents']
        date = json.loads(dumped_contents)
        date = date["dg_date"]
        model = None
        try:
            model = DailyGoals.objects.get(user=request.user, update_time=date)
            model.dumped_contents = dumped_contents
        except ObjectDoesNotExist:
            model = DailyGoals()
            model.user = request.user
            model.update_time = date
            model.dumped_contents = dumped_contents
        model.save()
        return JsonResponse({'status': '일일 연습 목표 설정 및 성취 평가 저장 완료'})
    except Exception as ex:
        print(ex)

def ltg_date_exsist(request):
    try :
        date = request.GET["date"]
        try:
            ltg_term_goal = LongTermGoals.objects.get(user=request.user, update_time=date)
            json =  ltg_term_goal.getDumpedContents()
            print(json)
            return JsonResponse(json)
        except ObjectDoesNotExist:
            return JsonResponse({'false':'false'})
    except Exception as ex:
        print(ex)

def dg_date_exsist(request):
    try:
        try:
            date = request.GET["date"]
            model = DailyGoals.objects.get(user=request.user,update_time = date)
            dumped_contents = json.loads(model.dumped_contents)
            print(dumped_contents)
            print(dumped_contents["dg_content".format()])
            return JsonResponse({"contents": dumped_contents["dg_content".format()],
                                 "archieved": dumped_contents['dg_achieved'.format()]})

        except ObjectDoesNotExist:
            return JsonResponse({})
    except Exception as ex:
        print(ex)

def diary_exsist(request):
    try :
        model = None
        try:
            model = Diary.objects.get(user=request.user, date=request.GET["date"],
                                      competition_level=request.GET["competition_level"])
            return JsonResponse({"dumped_contents": json.loads(model.dumped_contents),
                                 "competition_name":model.competition_name})
        except ObjectDoesNotExist:
            return JsonResponse({})
    except Exception as ex:
        print(ex)