#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from .models import GolfSwing, ShortGame, Putting
from .forms import GolfSwingForm, ShortGameForm, PuttingForm
from main.models import Member
from main.views import user_passes_test, has_permission_g2, has_permission_mypage
import re
import json
from django.core.exceptions import ObjectDoesNotExist

def extract_key_contents(contents_dict):
    comments_re = re.compile(r'^comment_(?P<i_idx>[0-9]+)_(?P<j_idx>[0-9]+)_(?P<k_idx>[0-9]+)$')
    drills_re = re.compile(r'^drill_(?P<i_idx>[0-9]+)_(?P<j_idx>[0-9]+)_(?P<k_idx>[0-9]+)$')
    key_contents = dict()
    for key, value in contents_dict.items():
        comments_re_result = comments_re.match(key)
        drills_re_result = drills_re.match(key)
        if comments_re_result is not None or drills_re_result is not None:
            # i_idx, j_idx: currently not used
            # i_idx = int(re_result.group('i_idx'))
            # j_idx = int(re_result.group('j_idx'))
            key_contents[key] = value
    return key_contents


def render_eval_page(request, template_name, model_cls):
    assert request.method == 'GET'
    if request.user.is_staff:
        if 'target_user_id' not in request.GET:
            return render(request, 'common/access_forbidden.html')
        else:
            target_user_id = request.GET['target_user_id']
    else:
        target_user_id = request.user.username
    context = {'target_user_id': target_user_id}
    try:
        model = model_cls.objects.get(user=request.user)
        context['record_exists'] = True
        context["categories"] = model.fill_contents()
        if model.video:
            json_videos = json.loads(model.video)
            videos = []
            for key in json_videos:
                videos.append(json.loads(json_videos.get(key)))
            context["videos"] = videos
    except ObjectDoesNotExist:
        context["categories"] = model_cls.get_categories()
    return render(request, template_name, context)


def update_eval_contents(request, form_cls , model):
    try:
        assert request.method == 'POST'
        if request.user.is_staff:
            if 'target_user_id' not in request.POST:
                return render(request, 'common/access_forbidden.html')
            else:
                target_user_id = request.POST['target_user_id']
        else:
            target_user_id = request.user.username
        model_instance = None
        try :
            model_instance = model.objects.get(user = request.user)
        except ObjectDoesNotExist:
            form = form_cls(request.POST)
            if not form.is_valid():
                return HttpResponse(form.errors)
            model_instance = form.save(commit=False)
            model_instance.user = request.user
        dumped_data = json.loads(request.POST['contents_dict'])
        if dumped_data["videos"]:
            video_dump = dict()
            for key in dumped_data["videos"]:
                video_dump[key] = json.dumps(dumped_data["videos"].get(key))
            model_instance.video = json.dumps(video_dump)
        else:
            model_instance.video = None
        contents = extract_key_contents(dumped_data)
        model_instance.dumped_contents = json.dumps(contents)
        model_instance.save()
        return JsonResponse({'status': 'success'})
    except Exception as ex:
        print(ex)

@login_required
@user_passes_test(has_permission_g2, "G2 이용 권한이 없습니다.")
def eval_golf_swing(request):
    if request.method == 'GET':
        return render_eval_page(request, 'g2/golf_swing.html', GolfSwing)
    else:   # request.method == 'POST':
        return update_eval_contents(request, GolfSwingForm,GolfSwing)


@login_required
@user_passes_test(has_permission_g2, "G2 이용 권한이 없습니다.")
def eval_short_game(request):
    if request.method == 'GET':
        return render_eval_page(request, 'g2/short_game.html', ShortGame)
    else:   # request.method == 'POST':
        return update_eval_contents(request, ShortGameForm,ShortGame)


@login_required
@user_passes_test(has_permission_g2, "G2 이용 권한이 없습니다.")
def eval_putting(request):
    if request.method == 'GET':
        return render_eval_page(request, 'g2/putting.html', Putting)
    else:  # request.method == 'POST':
        return update_eval_contents(request, PuttingForm, Putting)


@login_required
@user_passes_test(has_permission_mypage, "My Page 이용 권한이 없습니다.")
def profile(request):
    if request.method == 'GET':
        if request.user.is_staff:
            return render(request, 'common/access_forbidden.html')
        target_user = request.user
        context = {}
        for contents_name, model_cls in zip(['golf_swing', 'short_game', 'putting'], [GolfSwing, ShortGame, Putting]):
            # queried = model_cls.objects.filter(user=target_user).order_by('-update_time')
            queried = None
            result= None
            try :
                queried = model_cls.objects.get(user=request.user)
                result = queried.fill_contents()
            except ObjectDoesNotExist:
                queried = model_cls()
                result = queried.get_categories()

            # if queried.exists():
            #     result = queried[0].fill_contents()
            # else:
            #     result = model_cls.get_categories()


            # 비어있는 third category 제거
            for i, (first_category, second_categories) in enumerate(result):
                for j, (second_category, third_categories) in enumerate(second_categories):
                    new_third_categories = [[third_category, comment, drill]
                                            for third_category, comment, drill
                                            in third_categories
                                            if comment or drill]
                    result[i][1][j][1] = new_third_categories
            if queried.video:
                json_videos = json.loads(queried.video)
                videos = []
                for key in json_videos:
                    videos.append(json.loads(json_videos.get(key)))
                context[contents_name+"_videos"]=videos
                print(contents_name)
            context[contents_name] = result

        target_member = Member.objects.get(user=target_user)
        member_info = {
            'name': target_member.full_name,
            'sex': '남자' if target_member.sex == 'M' else '여자',
            'birth': target_member.birth,
            'handicap': target_member.handicap if target_member.handicap is not None else '-',
            'association': target_member.association,
        }
        context['member_info'] = member_info

        return render(request, 'g2/profile.html', context)
    elif request.method == 'POST':
        return render(request, 'common/access_forbidden.html')
    else:
        raise NotImplementedError


def update(request):
    if request.method == 'GET':
        pass
    else:   # request.method == 'POST':
        pass