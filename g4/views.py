# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main.models import Member
from main.views import user_passes_test, has_permission_g4, has_permission_mypage
from g4.models import OceanTest, Gmet, Tops, Fss, Acsi, CourseManagement
from g4.forms import OceanTestForm, GmetForm, TopsForm, FssForm, AcsiForm, CourseManagementForm
import json
import re
from django.core.exceptions import ObjectDoesNotExist

class StringManager:
    NO_RECORD = ''
    NO_COMMENT = ''
    NA = ''


class ViewManager:
    @staticmethod
    def get_scores_from_post(post):
        score_re = re.compile(r'^score_(?P<q_num>[0-9]+)$')
        scores = {}
        for key, value in post.items():
            re_result = score_re.match(key)
            if re_result is None:
                continue
            q_num = int(re_result.group('q_num'))
            scores[q_num] = int(value)
        return scores

    @staticmethod
    def render(request, template, model_cls, form_cls):
        return render(request, template, {'answer_labels': model_cls.survey_info.answer_labels,
                                          'answer_choices': model_cls.survey_info.answer_choices,
                                          'question_labels': model_cls.survey_info.question_labels,
                                          'form': form_cls(),
                                          })


    @staticmethod
    def submit(request, model_cls, form_cls):
        try:
            form = form_cls(request.POST)
            if not form.is_valid():
                return HttpResponse(form.errors)
            model = None
            try:
                model = model_cls.objects.get(user=request.user, update_time=request.POST["date"])
            except ObjectDoesNotExist:
                model = model_cls()
                print(model,model_cls)
                assert isinstance(model, model_cls)
                model.user = request.user
                print('aa')
                print(request.POST["date"])
                print(timezone.now)
                model.update_time = request.POST["date"]
                print(model)
            scores = ViewManager.get_scores_from_post(request.POST)
            assert len(scores) == model.survey_info.num_questions
            model.dumped_scores = json.dumps(scores)
            model.save()
            return JsonResponse(model.get_results())
            #error 'unicode' object has no attribute 'astimezone'
            #return JsonResponse({'success':'success'})
        except Exception as ex:
            print(ex)

@login_required
@user_passes_test(has_permission_g4, "G4 이용 권한이 없습니다.")
def ocean_test(request):
    return ViewManager.render(request, 'g4/ocean_test.html', OceanTest, OceanTestForm)

@login_required
@user_passes_test(has_permission_g4, "G4 이용 권한이 없습니다.")
def gmet(request):
    return ViewManager.render(request, 'g4/gmet.html', Gmet, GmetForm)

@login_required
@user_passes_test(has_permission_g4, "G4 이용 권한이 없습니다.")
def tops(request):
    return ViewManager.render(request, 'g4/tops.html', Tops, TopsForm)

@login_required
@user_passes_test(has_permission_g4, "G4 이용 권한이 없습니다.")
def fss(request):
    return ViewManager.render(request, 'g4/fss.html', Fss, FssForm)

@login_required
@user_passes_test(has_permission_g4, "G4 이용 권한이 없습니다.")
def acsi(request):
    return ViewManager.render(request, 'g4/acsi.html', Acsi, AcsiForm)

@login_required
@user_passes_test(has_permission_g4, "G4 이용 권한이 없습니다.")
def course_management(request):
    return ViewManager.render(request, 'g4/course_management.html', CourseManagement, CourseManagementForm)

@login_required
@user_passes_test(has_permission_g4, "G4 이용 권한이 없습니다.")
def ocean_test_submit(request):
    return ViewManager.submit(request, OceanTest, OceanTestForm)

@login_required
@user_passes_test(has_permission_g4, "G4 이용 권한이 없습니다.")
def gmet_submit(request):
    return ViewManager.submit(request, Gmet, GmetForm)

@login_required
@user_passes_test(has_permission_g4, "G4 이용 권한이 없습니다.")
def tops_submit(request):
    return ViewManager.submit(request, Tops, TopsForm)

@login_required
@user_passes_test(has_permission_g4, "G4 이용 권한이 없습니다.")
def fss_submit(request):
    return ViewManager.submit(request, Fss, FssForm)

@login_required
@user_passes_test(has_permission_g4, "G4 이용 권한이 없습니다.")
def acsi_submit(request):
    return ViewManager.submit(request, Acsi, AcsiForm)

@login_required
@user_passes_test(has_permission_g4, "G4 이용 권한이 없습니다.")
def course_management_submit(request):
    return ViewManager.submit(request, CourseManagement, CourseManagementForm)

@login_required
@user_passes_test(has_permission_mypage, "My Page 이용 권한이 없습니다.")
def profile(request):
    if request.method == 'GET':
        if request.user.is_staff:
            assert 'target_user_id' in request.GET
            is_admin = 1
            target_user_id = request.GET['target_user_id']
        else:
            assert 'target_user_id' not in request.GET
            is_admin = 0
            target_user_id = request.user.username
        target_user = User.objects.get(username=target_user_id)
        target_member = Member.objects.get(user=target_user)
        member_info = {
            'name': target_member.full_name,
            'sex': '남자' if target_member.sex == 'M' else '여자',
            'birth': target_member.birth or '-',
            'handicap': target_member.handicap if target_member.handicap is not None else '-',
            'association': target_member.association,
        }
        return render(request, 'g4/profile.html',
                      context={'is_admin': is_admin, 'target_user_id': target_user_id,
                               'member_info': member_info,
                               'factors_1': OceanTest.result_labels[0:5],
                               'factors_2': Gmet.result_labels,
                               'factors_3': Tops.result_labels,
                               'factors_4': Fss.result_labels,
                               'factors_5': Acsi.result_labels,
                               'factors_6': CourseManagement.result_labels})
    elif request.method == 'POST':
        assert 'target_user_id' in request.POST
        target_user_id = request.POST['target_user_id']
        assert User.objects.filter(username=target_user_id).exists()
        target_user = User.objects.get(username=target_user_id)
        assert request.user.is_staff or target_user_id == request.user.username

        titles = []
        labels = []
        num_attributes = []
        baseline_evaluations = []
        current_evaluations = []
        comments = []
        strategies = []

        for model_cls in [OceanTest, Gmet, Tops, Fss, Acsi, CourseManagement]:
            titles.append(model_cls.full_title)
            labels.append(model_cls.result_labels)
            num_attributes.append(len(model_cls.result_labels))
            queried = model_cls.objects.filter(user=target_user).order_by('-update_time')
            if queried.exists():
                baseline_evaluations.append(queried.reverse()[0].get_results())
                current_evaluations.append(queried[0].get_results())
                comments.append(queried[0].comment)
                strategies.append(queried[0].strategy)
            else:
                baseline_evaluations.append(StringManager.NO_RECORD)
                current_evaluations.append(StringManager.NO_RECORD)
                comments.append(StringManager.NO_COMMENT)
        is_admin = 1 if request.user.is_staff else 0
        return JsonResponse({'is_admin': is_admin,
                             'target_user_id': target_user_id,
                             'titles': titles,
                             'labels': labels,
                             'num_attributes': num_attributes,
                             'b_eval': baseline_evaluations,
                             'c_eval': current_evaluations,
                             'comments': comments,
                             'strategies': strategies})

@login_required
def update(request):
    try:
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            target_user_id = request.POST['target_user_id']
            idx = int(request.POST['idx'])
            comment = request.POST['comment']
            # if request.POST["strategy"]:
            #     strategy = request.POST['strategy']
            target_user = User.objects.get(username=target_user_id)
            model_cls = [OceanTest, Gmet, Tops, Fss, Acsi, CourseManagement][idx]
            queried = model_cls.objects.filter(user=target_user).order_by('-update_time')
            if queried.exists():
                print(len(queried))
                latest_instance = queried[0]
                latest_instance.comment = comment
                print(latest_instace)
                if isinstance(latest_instance,Acsi) or isinstance(latest_instance,CourseManagement):
                    latest_instance.strategy = request.POST["strategy"]
                latest_instance.save()
                status = 'success'
            else:
                status = 'no matching record instances'
            print(model_cls)
            return JsonResponse({
                'status': status
            })
    except Exception as ex:
        print(ex)