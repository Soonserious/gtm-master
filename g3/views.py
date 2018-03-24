# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from g3.forms import TeeShotForm, ApproachShotForm, FiftyFourShotForm, SeveGameForm, NineHoleForm, HoganGameForm, ScoringGameForm
from g3.models import TeeShot, ApproachShot, FiftyFourShot, SeveGame, NineHole, HoganGame, ScoringGame, PowerGameAnalysis, ScoringGameAnalysis

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main.models import Member
from main.views import user_passes_test, has_permission_g3, has_permission_mypage

import numpy as np
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
import datetime


class StringManager:
    NO_RECORD = ''
    NO_COMMENT = ''
    NA = ''


@login_required
@user_passes_test(has_permission_g3, "G3 이용 권한이 없습니다.")
def shot_challenge(request):
    # Division of shots in tee shot challenge
    tee_shot_div1 = map(lambda x: x + 1, range(10))
    tee_shot_div2 = map(lambda x: x + 11, range(3))
    tee_shot_div3 = map(lambda x: x + 14, range(1))

    # Division of shots in approach shot challenge
    approach_shot_div1 = ["6i", "5i", "7i", "4i", "8i", "3i / 5 Wood", "9i", "3 Wood", "P Wedge", "56 Wedge"]
    approach_shot_div2 = ["8i", "4i", "3 Wood"]
    approach_shot_div3 = ["6i"]

    # Divisions of shots in fifty four shot challenge
    fifty_four_shot_label1 = ["5 clubs 5 targets"]
    fifty_four_shot_row1 = ["9i", "7i", "5i", "우드", "드라이버"]
    fifty_four_shot_label2 = ["High", "Low", "오른쪽으로 휘기", "왼쪽으로 휘기", "A half shot (50% 샷)"]
    fifty_four_shot_row2 = ["8i", "6i", "4i", "우드", "드라이버"]
    fifty_four_shot_label3 = ["왼손잡이 샷 (7i)"]
    fifty_four_shot_row3 = ["7i", "7i", "7i", "7i", "7i"]
    fifty_four_shot_label4 = ["8번 아이언으로 샷을하고, 7i, 6i, 5i, 우드, 드라이버로 같은 지점을 케리 하는 샷을 한다"]
    fifty_four_shot_row4 = ["8i", "7i", "6i", "5i", "우드", "드라이버"]
    fifty_four_shot_label5 = ["두 발 모으고 샷 (7i), 왼발로 서서 샷 (7i), 두 눈 감고 샷 (7i)"]
    fifty_four_shot_row5 = ["7i", "7i", "7i"]
    fifty_four_shot_label6 = ["디봇에서의 샷 5개의 클럽을 이용한다"]
    fifty_four_shot_row6 = ["G", "9i", "7i", "5i", "우드"]
    fifty_four_shot_label7 = ["5 클럽 5 타겟"]
    fifty_four_shot_row7 = ["8i", "6i", "4i", "우드", "드라이버"]

    return render(request, 'g3/shot_challenge.html', {'tee_shot_div1': tee_shot_div1,
                                                  'tee_shot_div2': tee_shot_div2,
                                                  'tee_shot_div3': tee_shot_div3,
                                                  'approach_shot_div1': approach_shot_div1,
                                                  'approach_shot_div2': approach_shot_div2,
                                                  'approach_shot_div3': approach_shot_div3,
                                                      'fifty_four_shot_label1': fifty_four_shot_label1,
                                                      'fifty_four_shot_label2': fifty_four_shot_label2,
                                                      'fifty_four_shot_label3': fifty_four_shot_label3,
                                                      'fifty_four_shot_label4': fifty_four_shot_label4,
                                                      'fifty_four_shot_label5': fifty_four_shot_label5,
                                                      'fifty_four_shot_label6': fifty_four_shot_label6,
                                                      'fifty_four_shot_label7': fifty_four_shot_label7,
                                                      'fifty_four_shot_row1': fifty_four_shot_row1,
                                                      'fifty_four_shot_row2': fifty_four_shot_row2,
                                                      'fifty_four_shot_row3': fifty_four_shot_row3,
                                                      'fifty_four_shot_row4': fifty_four_shot_row4,
                                                      'fifty_four_shot_row5': fifty_four_shot_row5,
                                                      'fifty_four_shot_row6': fifty_four_shot_row6,
                                                      'fifty_four_shot_row7': fifty_four_shot_row7})


def tee_shot_submit(request):
    # Check validity and save the input data
    tee_shot_form = TeeShotForm(request.POST)
    if tee_shot_form.is_valid():
        try:
            tee_shot_model = TeeShot.objects.get(user=request.user, date=request.POST["date"])
            for filed in tee_shot_model._meta.get_fields():
                filed_name = str(filed)
                filed_name = filed_name.replace("g3.TeeShot.", "")
                if filed_name == "id":
                    continue
                if filed_name == "user":
                    continue
                if filed_name == "create_time":
                    continue
                filed = tee_shot_form.cleaned_data[filed_name]
        except ObjectDoesNotExist:
            tee_shot_model = tee_shot_form.save(commit=False)
            tee_shot_model.user = request.user

        tee_shot_model.save()
        return tee_shot_model.result()
    else:
        print(tee_shot_form.errors)
        return None

    return None


def approach_shot_submit(request):
    # Check validity and save the input data
    approach_shot_form = ApproachShotForm(request.POST)
    if approach_shot_form.is_valid():
        approach_shot_model = None
        try :
            approach_shot_model = ApproachShot.objects.get(user=request.user, date=request.POST["date"])
            for filed in approach_shot_model._meta.get_fields():
                filed_name = str(filed)
                filed_name = filed_name.replace("g3.ApproachShot.", "")
                if filed_name == "id":
                    continue
                if filed_name == "user":
                    continue
                if filed_name == "create_time":
                    continue
                filed = approach_shot_form.cleaned_data[filed_name]

        except ObjectDoesNotExist:
            approach_shot_model = approach_shot_form.save(commit=False)
            approach_shot_model.user = request.user
        approach_shot_model.save()
        return approach_shot_model.result()
    else:
        print(approach_shot_form.errors)
        return None

    return None


def fifty_four_shot_submit(request):
    # Check validity and save the input data
    fifty_four_shot_form = FiftyFourShotForm(request.POST)
    if fifty_four_shot_form.is_valid():
        fifty_four_shot_model = None
        try :
            fifty_four_shot_model = FiftyFourShot.objects.get(user=request.user,date=request.POST["date"])
            for filed in fifty_four_shot_model._meta.get_fields():
                filed = fifty_four_shot_model.cleaned_data[filed_name]

        except ObjectDoesNotExist :
            fifty_four_shot_model = fifty_four_shot_form.save(commit=False)
            fifty_four_shot_model.user = request.user
        fifty_four_shot_model.save()
    else:
        print(fifty_four_shot_form.errors)
        return None

    return fifty_four_shot_model.result()


@login_required
@user_passes_test(has_permission_g3, "G3 이용 권한이 없습니다.")
def short_game(request):
    # Division of shots in seve game
    seve_game_label1 = ["1야드", "4야드", "7야드", "10야드"]
    seve_game_label2 = ["15야드", "20야드", "25야드", "30야드"]
    seve_game_label3 = ["5야드", "10야드", "15야드", "20야드"]
    seve_game_label4 = ["3야드", "8야드", "15야드", "25야드"]
    seve_game_label5 = ["15야드 이상"]
    seve_game_label6 = [""]

    nine_hole_label = ["프린지에서 Putt – 45ft(15야드).",
                       "그린 엣지로부터 5 야드 거리에서 Chip Shot – 30ft(10야드).",
                       "짧은 거리의 bunker shot – 20~30ft(7~10야드).",
                       "그린 엣지로부터 10 야드 거리에서 Pitch Shot  – 60ft(20야드).",
                       "프린지에서 Putt – 60 ft(20야드).",
                       "그린 엣지로부터 5 야드 거리에서 Chip Shot – 75ft(25야드).",
                       "중간 거리의 bunker shot – 50~60ft(15~20야드).",
                       "그린 엣지로부터 25 야드 거리에서 Pitch Shot – 120ft(40야드).",
                       "벙커 너머 공간이 부족한 어려운 위치에 있는 홀로의 Flop or Lob Shot – 볼 드롭"]

    return render(request, 'g3/short_game.html', {'seve_game_label1': seve_game_label1,
                                                  'seve_game_label2': seve_game_label2,
                                                  'seve_game_label3': seve_game_label3,
                                                  'seve_game_label4': seve_game_label4,
                                                  'seve_game_label5': seve_game_label5,
                                                  'seve_game_label6': seve_game_label6,
                                                  'nine_hole_label': nine_hole_label})


def seve_game_submit(request):
    # Check validity and save the input data
    seve_game_form = SeveGameForm(request.POST)
    if seve_game_form.is_valid():
        seve_game_model =None
        try :
            seve_game_model = SeveGame.objects.get(user=request.user ,date=request.POST['date'])
            for filed in seve_game_model._meta.get_fields():
                # filed_name = str(filed)
                # filed_name = filed_name.replace("g3.SeveGame.", "")
                # if filed_name == "id":
                #     continue
                # if filed_name == "user":
                #     continue
                # if filed_name == "create_time":
                #     continue
                filed = seve_game_model.cleaned_data[filed_name]
        except ObjectDoesNotExist:
            seve_game_model = seve_game_form.save(commit=False)
            seve_game_model.user = request.user
            seve_game_model.date= request.POST["date"]

        seve_game_model.save()
        return seve_game_model.result()
    else:
        print(seve_game_form.errors)
        return None

    return None


def nine_hole_submit(request):
    # Check validity and save the input data
    nine_hole_form = NineHoleForm(request.POST)
    try:

        if nine_hole_form.is_valid():
            nine_hole_model = None
            try:
                nine_hole_model = NineHole.objects.get(user=request.user, date=request.POST["date"])
                for filed in nine_hole_model._meta.get_fields():
                    # filed_name = str(filed)
                    # print(filed_name)
                    # filed_name = filed_name.replace("g3.NineHole.", "")
                    # if filed_name == "id":
                    #     continue
                    # if filed_name == "user":
                    #     continue
                    # if filed_name == "create_time":
                    #     continue
                    filed = nine_hole_form.cleaned_data[filed_name]
            except ObjectDoesNotExist:
                date = None;
                nine_hole_model = nine_hole_form.save(commit=False)
                nine_hole_model.user = request.user
                nine_hole_model.date = request.POST["date"]

            nine_hole_model.save()
        else:
            return None

        return nine_hole_model.result()
    except Exception as ex:
        print(ex)

@login_required
@user_passes_test(has_permission_g3, "G3 이용 권한이 없습니다.")
def putting_game(request):
    # Division of shots in hogan game
    hogan_game_label1 = ["3", "5", "7", "9", "11", "13"]
    hogan_game_label2 = ["15", "18", "21", "24", "27", "30"]
    hogan_game_label3 = ["35", "40", "45", "50", "55", "60"]

    return render(request, 'g3/putting_game.html', {'hogan_game_label1': hogan_game_label1,
                                                    'hogan_game_label2': hogan_game_label2,
                                                    'hogan_game_label3': hogan_game_label3})


def hogan_game_submit(request):
    # Check validity and save the input data
    hogan_game_form = HoganGameForm(request.POST)
    if hogan_game_form.is_valid():
        hogan_game_model = None
        try:
            hogan_game_model = HoganGame.objects.get(user=request.user, date=request.POST["date"])
            for filed in hogan_game_model._meta.get_fields():
                filed_name = str(filed)
                # filed_name = filed_name.replace("g3.HoganGame.", "")
                # if filed_name == "id":
                #     continue
                # if filed_name == "user":
                #     continue
                # if filed_name == "create_time":
                #     continue
                filed = hogan_game_form.cleaned_data[filed_name]

        except:
            hogan_game_model = hogan_game_form.save(commit=False)
            hogan_game_model.user = request.user
            hogan_game_form.date = request.POST["date"]
        hogan_game_model.save()
    else:
        print(hogan_game_form.errors)
        return None

    return hogan_game_model.result()


@login_required
@user_passes_test(has_permission_g3, "G3 이용 권한이 없습니다.")
def scoring_game(request):
    # Division of shots in scoring game
    scoring_game_label1 = ["Up Hill", "Down Hill", "Side L-R", "Side R-L"]
    scoring_game_label2 = ["5 tries"]
    scoring_game_label3 = ["5 tries"]
    scoring_game_label4 = ["5 tries"]

    return render(request, 'g3/scoring_game.html', {'scoring_game_label1': scoring_game_label1,
                                                    'scoring_game_label2': scoring_game_label2,
                                                    'scoring_game_label3': scoring_game_label3,
                                                    'scoring_game_label4': scoring_game_label4})


def scoring_game_submit(request):
    # Check validity and save the input data
    scoring_game_form = ScoringGameForm(request.POST)
    if scoring_game_form.is_valid():
        scoring_game_model = None
        try:
            scoring_game_model = ScoringGame.objects.get(user=request.user, date=request.POST["date"])
            for filed in scoring_game_model._meta.get_fields():
                filed_name = str(filed)
                # filed_name = filed_name.replace("g3.ScoringGame.", "")
                # if filed_name == "id":
                #     continue
                # if filed_name == "user":
                #     continue
                # if filed_name == "create_time":
                #     continue
                # if filed_name == "date":
                #     continue
                filed = scoring_game_form.cleaned_data[filed_name]
        except ObjectDoesNotExist:
            scoring_game_model = scoring_game_form.save(commit=False)
            scoring_game_model.user = request.user
            scoring_game_model.date = request.POST["date"]
        scoring_game_model.save()
    else:
        print(scoring_game_form.errors)
        return None

    return scoring_game_model.result()


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
        row_titles = {
            'p0t0': ['Tee Shot Challenge', 'Approach Shot Challenge', '54 Shot Challenge'],
            'p1t0': ['Nine Hole Scoring Ability Test', 'The Seve Game', 'The Hogan Game', 'Scoring Game Skill Test'],
            'p1t1': ['Chip Shot', 'Pitch Shot', 'Bunker Shot'],
            'p1t2': ['Short Putt', 'Middle Putt', 'Long Putt'],
        }
        return render(
            request,
            'g3/profile.html',
            context={'is_admin': is_admin, 'target_user_id': target_user_id, 'member_info': member_info, 'row_titles': row_titles}
        )
    elif request.method == 'POST':
        try:
            assert 'target_user_id' in request.POST
            target_user_id = request.POST['target_user_id']
            assert User.objects.filter(username=target_user_id).exists()
            target_user = User.objects.get(username=target_user_id)
            assert request.user.is_staff or target_user_id == request.user.username

            num_parts = 2  # Power Game Profile, Scoring Game Profile
            num_tables = [1, 3]
            # pi: part index, _: table index(ti)
            prev_levels = [[[] for _ in range(num_tables[pi])] for pi in range(num_parts)]
            curr_levels = [[[] for _ in range(num_tables[pi])] for pi in range(num_parts)]
            level_history = [[[] for _ in range(num_tables[pi])] for pi in range(num_parts)]
            comments = []
            strategies = []
            standardTime = datetime.datetime.now()
            standardTime = standardTime - datetime.timedelta(days=180);
            for (pi, ti), model_cls in zip(
                    [(0, 0)] * 3 + [(1, 0)] * 4,
                    [
                        TeeShot, ApproachShot, FiftyFourShot,  # p0t0
                        NineHole, SeveGame, HoganGame, ScoringGame  # p0t1
                    ]
            ):
                queried = model_cls.objects.filter(user=target_user,
                                                   date__gte=standardTime).order_by(
                    '-date').distinct()
                distinct_records = []
                dates = []
                for record in queried:
                    if record.date in dates:
                        continue
                    dates.append(record.date)
                    distinct_records.append(record)
                num_records = len(distinct_records)
                latest_levels = []
                latest_scores = []
                latest_dates = []
                for i in range(min(num_records, 10)):
                    result = distinct_records[i].result_non_json()
                    latest_levels.append(result['level'])
                    latest_scores.append(result['score'])
                    latest_dates.append(result['date'].strftime('%Y-%m-%d'))

                curr_score_avg = np.mean(latest_scores[:min(num_records, 3)]) if latest_scores else None
                curr_level = model_cls.get_level_by_score(
                    curr_score_avg) if curr_score_avg is not None else StringManager.NA

                oldest_scores = [distinct_records[-1 - i].result_non_json()['score'] for i in
                                 range(min(num_records, 3))]
                prev_score_avg = np.mean(oldest_scores) if oldest_scores else None
                prev_level = model_cls.get_level_by_score(
                    prev_score_avg) if prev_score_avg is not None else StringManager.NA

                curr_levels[pi][ti].append(curr_level)
                prev_levels[pi][ti].append(prev_level)
                level_history[pi][ti].append({'levels': latest_levels[::-1], 'dates': latest_dates[::-1]})

            attr_names = [
                ['chipping_level', 'chipping_score', ScoringGame.get_level_by_score_chipping],
                ['pitching_level', 'pitching_score', ScoringGame.get_level_by_score_pitching],
                ['bunker_level', 'bunker_score', ScoringGame.get_level_by_score_bunker],  # p1t1
                ['short_putting_level', 'short_putting_score', ScoringGame.get_level_by_score_short_putting],
                ['middle_putting_level', 'middle_putting_score', ScoringGame.get_level_by_score_middle_putting],
                ['long_putting_level', 'long_putting_score', ScoringGame.get_level_by_score_long_putting],  # p1t2
            ]
            latest_levels = [[] for _ in range(len(attr_names))]
            latest_scores = [[] for _ in range(len(attr_names))]
            latest_dates = [[] for _ in range(len(attr_names))]
            oldest_levels = [[] for _ in range(len(attr_names))]
            oldest_scores = [[] for _ in range(len(attr_names))]
            queried = ScoringGame.objects.filter(user=target_user, date__gte=standardTime).order_by('-date', '-create_time')
            distinct_records = []
            dates = []
            for record in queried:
                if record.date in dates:
                    continue
                dates.append(record.date)
                distinct_records.append(record)
            num_records = len(distinct_records)
            for qi in range(min(num_records, 10)):
                result = distinct_records[qi].result_non_json()
                for ai, (attr_level, attr_score, _) in enumerate(attr_names):
                    latest_levels[ai].append(result[attr_level])
                    latest_scores[ai].append(result[attr_score])
                    latest_dates[ai].append(result['date'].strftime('%Y-%m-%d'))
            for qi in range(min(num_records, 3)):
                result = distinct_records[-1 - qi].result_non_json()
                for ai, (attr_level, attr_score, _) in enumerate(attr_names):
                    oldest_levels[ai].append(result[attr_level])
                    oldest_scores[ai].append(result[attr_score])

            for (pi, ti), (ai, (_, __, scoring_fn)) in zip(
                    [(1, 1)] * 3 + [(1, 2)] * 3,
                    enumerate(attr_names)
            ):
                curr_score_avg = np.mean(latest_scores[ai][:min(num_records, 3)]) if latest_scores[ai] else None
                curr_level = scoring_fn(curr_score_avg) if curr_score_avg is not None else StringManager.NA
                prev_score_avg = np.mean(oldest_scores[ai]) if oldest_scores[ai] else None
                prev_level = scoring_fn(prev_score_avg) if prev_score_avg is not None else StringManager.NA
                curr_levels[pi][ti].append(curr_level)
                prev_levels[pi][ti].append(prev_level)
                level_history[pi][ti].append({'levels': latest_levels[ai][::-1], 'dates': latest_dates[ai][::-1]})

            for model_cls in [PowerGameAnalysis, ScoringGameAnalysis]:
                queried = model_cls.objects.filter(user=target_user, update_time__gte=standardTime).order_by('-update_time')
                if queried.exists():
                    comments.append(queried[0].comment)
                    strategies.append(queried[0].comment)
                else:
                    comments.append(StringManager.NO_RECORD)
                    strategies.append(StringManager.NO_RECORD)

            is_admin = 1 if request.user.is_staff else 0
            ds_labels = {
                'p0t0': ['Tee Shot Challenge', 'Approach Shot Challenge', '54 Shot Challenge'],
                'p1t0': ['Nine Hole Scoring Ability Test', 'The Seve Game', 'The Hogan Game',
                         'Scoring Game Skill Test'],
                'p1t1': ['Chip Shot', 'Pitch Shot', 'Bunker Shot'],
                'p1t2': ['Short Putt', 'Middle Putt', 'Long Putt'],
            }

            return_dict = {
                'is_admin': is_admin,
                'ds_labels': ds_labels,
                'target_user_id': target_user_id,
                'num_parts': num_parts,
                'num_tables': num_tables,
                'curr_levels': curr_levels,
                'prev_levels': prev_levels,
                'level_history': level_history,
                'comments': comments,
            }

            return JsonResponse(return_dict)
        except Exception as ex:
            print(ex)

@login_required
def update(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        target_user_id = request.POST['target_user_id']
        idx = int(request.POST['idx'])
        comment = request.POST['comment'] if 'comment' in request.POST else None
        strategy = request.POST['strategy'] if 'strategy' in request.POST else None
        target_user = User.objects.get(username=target_user_id)
        model_cls = [PowerGameAnalysis, ScoringGameAnalysis][idx]
        queried = model_cls.objects.filter(user=target_user).order_by('-update_time')
        if queried.exists():
            instance = queried[0]
            status = 'updated'
        else:
            instance = model_cls()
            instance.user = target_user
            status = 'created'
        if comment is not None:
            instance.comment = comment
        if strategy is not None:
            instance.strategy = strategy
        instance.save()
        return JsonResponse({
            'status': status
        })

def date_exsist(request):

    date = request.GET["date"]
    text = request.GET["text"]
    target_user = request.user
    result = None

    try:
        if text == "Tee Shot Challenge" :
            try :
                result = TeeShot.objects.get(user=target_user.id, date=date)
            except :
                result = None
        elif text == 'Approach Shot Challenge':
            try :
                result = ApproachShot.objects.get(user=target_user, date=date)
            except :
                result = None
        elif text == '54 Shot Challenge' :
            try :
                result = FiftyFourShot.objects.get(user=target_user, date=date)
            except :
                result = None
        elif text =='9 Hole Scoring Aility Test' :
            try:
                result = NineHole.objects.get(user=target_user, date=date)
                print(result)
            except:
                result = None
        elif text =='Seve Game':
            try:
                result = SeveGame.objects.get(user=target_user, date= date)
            except:
                result = None
        elif text =='Scoring Game Skill Test':
            try:
                result = ScoringGame.objects.get(user=target_user, date=date)
            except:
                result = None
        elif text =='Hogan Game':
            try:
                result = HoganGame.objects.get(user=target_user, date=date)
            except:
                result = None;
        if result is not None:
            return JsonResponse({"result" : "success",
                                "tuple" : model_to_dict(result)})
        return JsonResponse({})
    except Exception as ex :
        print(ex)
