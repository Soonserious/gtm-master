#-*- coding:utf-8 -*-
import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import JsonResponse, Http404

from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .forms import *
from .models import *
from main.models import Member
from main.views import user_passes_test, has_permission_g1, has_permission_mypage
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt



def info(rr):
    stat = rr.get_stat()
    return {'rr': rr,
            'date': rr.date,
            'course': rr.course.field.name,
            'score': stat['score'],
            'fairway_hit': stat['fairway_hit'],
            'putt': stat['putt'],
            'gir': stat['gir'] / 18.0 * 100,
            'putt_gir': 1.0 * stat['putt_gir'] / stat['gir'] if stat['gir'] != 0 else 0,
            'up_and_down': 100.0 * stat['up_and_down'] / (18 - stat['gir']) if (18 - stat['gir']) != 0 else 0,
            'bunker': sum(rr.getbunker()),
            'sand_save': 100.0 * stat['sand_save'] / sum(rr.getbunker()) if sum(rr.getbunker()) != 0 else 0,
            'proximity': stat['proximity'],
            'birdie': stat['birdie'],
            'bogey': stat['bogey'],
            'double_bogey_or_more': stat['double_bogey_or_more'],
            'bounce_back': 100.0 * stat['bounce_back'] / stat['bogey_or_more'] if stat['bogey_or_more'] != 0 else 0,
            'driving_distance': stat['driving_distance'],
            'penalty': stat['penalty'],}


def average(rrs):
    ret = {}
    x = [info(rr) for rr in rrs]
    if len(x) == 0:
        return

    # 라운드 별 평균
    keys = ['score',
            'fairway_hit',
            'putt',
            'gir',
            'proximity',
            'birdie',
            'bogey',
            'double_bogey_or_more',
            'bunker',
            'driving_distance',
            'penalty']
    for key in keys:
        _sum = 0.0
        for r in x:
            _sum += r[key]
        ret[key] = _sum / len(x)

    # 해당 홀의 평균
    putt_gir_sum = 0
    gir_sum = 0
    up_and_down_sum = 0
    sand_save_sum = 0
    bunker_sum = 0
    bounce_back_sum = 0
    bogey_or_more_sum = 0
    for rr in rrs:
        stat = rr.get_stat()

        putt_gir_sum += stat['putt_gir']
        gir_sum += stat['gir']
        up_and_down_sum += stat['up_and_down']
        sand_save_sum += stat['sand_save']
        bunker_sum += sum(rr.getbunker())
        bounce_back_sum += stat['bounce_back']
        bogey_or_more_sum += stat['bogey_or_more']

    non_gir_sum = 18 * len(x) - gir_sum
    ret['putt_gir'] = putt_gir_sum / gir_sum if gir_sum != 0 else 0
    ret['up_and_down'] = 100.0 * up_and_down_sum / non_gir_sum if non_gir_sum != 0 else 0
    ret['sand_save'] = 100.0 * sand_save_sum / bunker_sum if bunker_sum != 0 else 0
    ret['bounce_back'] = 100.0 * bounce_back_sum / bogey_or_more_sum if bogey_or_more_sum != 0 else 0

    return ret


def minus(cr, avg):
    forward_keys = ["score", "putt", "putt_gir", "bunker", "proximity", "bogey", "double_bogey_or_more", "penalty"]
    backward_keys = ["fairway_hit", "gir", "up_and_down", "sand_save", "birdie", "bounce_back", "driving_distance"]
    ret = {}
    for key in forward_keys:
        ret[key] = cr.__dict__[key] - avg[key]
    for key in backward_keys:
        ret[key] = avg[key] - cr.__dict__[key]
    return ret


def handicap(rrs):
    x = [(rr.get_stat()['score'] - rr.course.course_rating) * 113.0 / rr.course.slope_rating if rr.course.slope_rating != 0 else 0 for rr in rrs]
    if len(x) == 0:
        return ''
    else:
        return sum(sorted(x)[:10]) / len(x[:10]) * 0.96


@login_required
@user_passes_test(has_permission_g1, "G1 이용 권한이 없습니다.")
def round(request):
    try :
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

        round_posted = RoundingResult.objects.filter(user=request.user).count()
        rrs = RoundingResult.objects.filter(user=request.user).order_by('-date', '-create_time')[:20]
        best_10 = sorted(rrs, key=lambda rr: sum(rr.getscore()))[:10]
        return render(request, 'g1/round.html', {'member_info': member_info,
                                                 'recent': [info(rr) for rr in rrs],
                                                 'recent_avg': average(rrs),
                                                 'best_10': [info(rr) for rr in best_10],
                                                 'best_10_avg': average(best_10),
                                                 'round_posted': round_posted,
                                                 'handicap': handicap(rrs)})
    except Exception as ex:
        print(ex)

@login_required
@user_passes_test(has_permission_mypage, "My Page 이용 권한이 없습니다.")
def profile(request):
    cr = Criteria.objects.first()
    if not cr:
        cr = Criteria()

    if request.user.is_staff:
        is_admin = 1
        target_user_id = request.GET['target_user_id']
    else:
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

    round_posted = RoundingResult.objects.filter(user=target_user).count()
    if round_posted == 0:
        return render(request,
                      'g1/profile.html',
                      {'member_info': member_info, 'round_posted': round_posted})

    rrs = RoundingResult.objects.filter(user=target_user).order_by('-date', '-create_time')[:20]
    avg = average(rrs)

    queried = RoundingResult.objects.filter(user=target_user).order_by('-date', '-create_time')
    if queried.exists():
        comment = queried[0].comment
    else:
        comment = ''

    par3_score = 0
    par3_count = 0
    par4_score = 0
    par4_count = 0
    par5_score = 0
    par5_count = 0

    holes = 0
    birdie_count = 0
    par_count = 0
    bogey_count = 0
    double_bogey_or_more_count = 0
    for rr in rrs:
        pars = rr.course.getpars()
        score = rr.getscore()

        par3 = list(map(operator.eq, pars, [3] * len(pars)))
        par3_score += sum(map(operator.mul, par3, score))
        par3_count += sum(par3)
        par4 = list(map(operator.eq, pars, [4] * len(pars)))
        par4_score += sum(map(operator.mul, par4, score))
        par4_count += sum(par4)
        par5 = list(map(operator.eq, pars, [5] * len(pars)))
        par5_score += sum(map(operator.mul, par5, score))
        par5_count += sum(par5)

        birdie_count += sum(map(operator.gt, pars, score))
        par_count += sum(map(operator.eq, pars, score))
        bogey_count += sum(map(operator.eq, [par + 1 for par in pars], score))
        double_bogey_or_more_count += sum(map(operator.le, [par + 2 for par in pars], score))
        holes += len(pars)

    return render(request, 'g1/profile.html',
                  {
                      'member_info': member_info,
                      'handicap': handicap(rrs),
                      'cr': cr,
                      'avg': avg,
                      'minus': minus(cr, avg),
                      'round_posted': round_posted,
                      'par3': 1.0 * par3_score / par3_count if par3_count != 0 else 0,
                      'par4': 1.0 * par4_score / par4_count if par4_count != 0 else 0,
                      'par5': 1.0 * par5_score / par5_count if par5_count != 0 else 0,
                      'birdie': 100.0 * birdie_count / holes if holes != 0 else 0,
                      'par': 100.0 * par_count / holes if holes != 0 else 0,
                      'bogey': 100.0 * bogey_count / holes if holes != 0 else 0,
                      'double_bogey_or_more': 100.0 * double_bogey_or_more_count / holes if holes != 0 else 0,
                      'target_user_id': target_user_id,
                      'comment': comment,
                      'is_admin': is_admin
                  })


def update(request):
    if request.method == 'GET':
        pass
    else:
        target_user_id = request.POST['target_user_id']
        target_user = User.objects.get(username=target_user_id)
        comment = request.POST['comment']
        queried = RoundingResult.objects.filter(user=target_user).order_by('-create_time')
        if queried.exists():
            last_instance = queried[0]
            last_instance.comment = comment
            last_instance.save()
        return JsonResponse({'status': '코멘트 업데이트 성공'})


@login_required
@user_passes_test(has_permission_g1, "G1 이용 권한이 없습니다.")
def round_result(request):
    return render(request, 'g1/round_result.html', {})


@login_required
@user_passes_test(has_permission_g1, "G1 이용 권한이 없습니다.")
def round_result_add(request):
    print(request)
    try:
        course = get_object_or_404(Course, id=request.GET["course_id"])
        rrf = RoundingResultForm()
        rr = None
        stat = None
        return render(request,
                      'g1/round_result_add.html',
                      {'course': course, 'rrf': rrf, 'rr': rr, 'stat': stat})
    except Exception as ex:
        print(ex)

@login_required
@user_passes_test(has_permission_g1, "G1 이용 권한이 없습니다.")

def round_result_add_submit(request):
    try:
        if request.method == 'POST':
            rrf = RoundingResultForm(request.POST["data"])
            if not rrf.is_valid():
                print(rrf.errors)
                raise Http404('form is not valid')

            # rr = RoundingResult.objects.filter(user=request.user, course=course, time=rrf.cleaned_data['time']).first()
            rr = rrf.save(commit=False)
            rr.user = request.user
            rr.course = course
            rr.setscore(rrf.score())
            rr.setdriving_distance(rrf.driving_distance())
            rr.setfairway_hit(rrf.fairway_hit())
            rr.setputt(rrf.putt())
            rr.setbunker(rrf.bunker())
            rr.setpenalty(rrf.penalty())
            rr.setproximity(rrf.proximity())
            rr.save()

            initial = {}
            for x in range(1, 19):
                initial['score_%02d' % x] = rr.getscore()[x - 1]
                initial['fairway_hit_%02d' % x] = rr.getfairway_hit()[x - 1]
                initial['putt_%02d' % x] = rr.getputt()[x - 1]
                initial['bunker_%02d' % x] = rr.getbunker()[x - 1]

                initial['driving_distance_%02d' % x] = rr.getdriving_distance()[x - 1]
                initial['penalty_%02d' % x] = rr.getpenalty()[x - 1]
                initial['proximity_%02d' % x] = rr.getproximity()[x - 1]
            stat = rr.get_stat()

            user = User.objects.get(username=request.user.username)
            member = Member.objects.get(user=user)
            rrs = RoundingResult.objects.filter(user=request.user).order_by('-date', '-create_time')[:20]
            member.handicap = handicap(rrs)
            member.save()

        return JsonResponse({"result" : "save"})
    except Exception as ex:
        print(ex)

def field_info(request):
    try:
        if request.method == 'GET':
            print("field_info" + request.GET['field_name'])
            fields = GolfField.objects.filter(name__contains=request.GET['field_name'])
            x = {field.id: {
                'name': field.name,
                'tee_types': [val['tee_type'] for val in field.course_set.all().values('tee_type')]
            }
                for field in fields}
            return JsonResponse(x)
    except Exception as ex :
        print(ex)

@login_required
@user_passes_test(has_permission_g1, "G1 이용 권한이 없습니다.")
def field_add(request):
    try:
        if request.method == 'POST':
            gff = GolfFieldForm(request.POST)
            if gff.data['name']:
                queried = GolfField.objects.filter(name=gff.data['name'])
            else:
                queried = GolfField.objects.all()
            if queried.exists():
                instance = queried[0]
                instance.type = gff.data['type']
                instance.phone_number = gff.data['phone_number']
                instance.address = gff.data['address']
                instance.save()
            else:
                if not gff.is_valid():
                    raise Http404('form validation error')
                gff.save()

        gff = GolfFieldForm()
        fcf = FindCourseForm()
        cf = CourseForm()
        return render(request, 'g1/field_add.html', {'golf_field_form': gff,
                                                     'find_course_form': fcf,
                                                     'course_form': cf})
    except Exception as ex:
        print(ex)

def course_info(request):
    # field = get_object_or_404(GolfField, id=field_id)
    # TODO : tee_type check; actually not needed.
    field_id = request.GET["field_id"]
    tee_type = request.GET["tee_type"]
    print("field_id : " + field_id + "tee_type : " + tee_type)
    try:
        c = Course.objects.get(field=field_id, tee_type=tee_type)
        return JsonResponse({
            'course_exists': True,
            'course_id': c.id,
            'course_rating': c.course_rating,
            'slope_rating': c.slope_rating,
            'hole_name_0': c.hole_name_0,
            'hole_name_1': c.hole_name_1,
            'yards': c.getyards(),
            'pars': c.getpars(),
            'handicaps': c.gethandicaps(),
            'is_staff': request.user.is_staff,
        })
    except Course.DoesNotExist:
        return JsonResponse({})


@login_required
@user_passes_test(has_permission_g1, "G1 이용 권한이 없습니다.")
def course_add(request):
    try:
        # TODO : tee_type check; actually not needed.

        if request.method != 'POST':
            raise Http404('course add should be post')
        cf = CourseForm(request.POST)
        if not cf.is_valid():
            print(cf.errors)
            raise Http404('Not valid form')

        field_id = request.POST["field_id"]
        tee_type = request.POST["tee_type"]
        print("course_add field_id : " + field_id + "tee_type  "+ tee_type)
        field = get_object_or_404(GolfField, id=field_id)
        course = None;
        try:
            course = Course.objects.get(field=field_id, tee_type=tee_type)
        except Course.DoesNotExist:
            cf = CourseForm(request.POST, instance=course)
            course = cf.save(commit=False)
            course.field = field
            course.tee_type = tee_type
        course.setyards(cf.yards())
        course.setpars(cf.pars())
        course.sethandicaps(cf.handicaps())
        course.save()
        return redirect(reverse('g1_field_add'))
    except Exception as ex:
        print(ex)
    # course, created = Course.objects.get_or_create(
    #    field=cf.cleaned_data['field'],
    #    tee_type=cf.cleaned_data['tee_type'],
    #    defaults={'course_rating' : cf.cleaned_data['course_rating'],
    #              'slope_rating' : cf.cleaned_data['slope_rating']
    #    }
    # )


@staff_member_required
def criteria(request):
    cr = Criteria.objects.first()
    if request.method == 'POST':
        cf = CriteriaForm(request.POST, instance=cr)
        if cf.is_valid():
            cf.save()
    else:
        cf = CriteriaForm(instance=cr)

    return render(request, 'g1/criteria.html', {'form': cf})


def field_remove(request):
    if request.method == 'POST':
        if request.POST["field_name"]:
            golfField = GolfField.objects.get(name__contains=request.POST["field_name"])
        else :
            golfField = GolfField.objects.all()
    else :
        golfField = GolfField.objects.all()
    return render(request, 'g1/field_remove.html',{'fields' : golfField})

def view_course(request):
    course = get_object_or_404(Course, id=request.GET["course_id"])
    return render(request,'g1/view_course.html',{'course': course})

def course_remove(request):
    print(request.GET["course_id"])
    try:
        course = Course.objects.get(id=request.GET["course_id"])
        course.delete()
        return JsonResponse({"result" : "success"})
    except Course.DoesNotExist:
        return JsonResponse()

def remove_filed_and_course(request):
    try:
        course = Course.objects.get(field_id = request.GET["field_id"])
        course.delete()
    except:
        print(request.GET["field_id"])
    try:
        field = GolfField.objects.get(id=request.GET["field_id"])
        field.delete()
        return JsonResponse({"result": "success"})
    except:

        return JsonResponse()

def AVG_bride(request):
    try:
        return render(request, 'g1/AVG_bride.html')
    except Exception as ex:
        print(ex)

def play_rythm(request):
   try:
       json = {}
       try:
           quried = RoundingResult.objects.filter(user=request.user).order_by("-date")
           size = min(len(quried),10)
           quired = quired[:size]
           part_one = {}
           part_two = {}
           part_three = {}
           for i in range(1,19):
               part_one["part_one_"+str(i)]=0
           for i in range(1,7):
               part_two["part_two_"+str(i)]=0
           for i in range(1,3):
               part_three["part_three_"+str(i)]=0
           for roundingResult in quried:
                for score, par, round in zip(roundingResult.getscore(),roundingResult.course.getpars(),range(1,19)):
                    part_one["part_one_" + str(round)] += (par-score)
                round_step_result=0
                for score, par, round in zip(roundingResult.getscore(),roundingResult.course.getpars(),range(1,19)):
                        round_step_result += (par-score)
                        if(round%3 == 0):
                            # print(round_step_result/3)
                            part_two["part_two_"+str(round/3)] += round_step_result/3
                            round_step_result = 0
                round_step_result = 0
                for score, par, round in zip(roundingResult.getscore(),roundingResult.course.getpars(),range(1,19)):
                        round_step_result += (par-score)
                        if(round%9 == 0):
                            # print(round_step_result/3)
                            part_three["part_three_"+str(round/9)] += round_step_result/9
                            round_step_result = 0
           one = []
           two =[]
           three =[]
           for i in range(1, 19):
               one.append( part_one["part_one_" + str(i)] / size)

           for i in range(1, 7):
               two.append(part_two["part_two_" + str(i)] /size)

           for i in range(1, 3):
               three.append(part_three["part_three_" + str(i)]/size)

       except ObjectDoesNotExist:
           print()
       return render(request, 'g1/play_rythm.html' , {"part_one" : one,
                                                      "part_two" : two,
                                                      "part_three" : three})
   except Exception as ex:
       print(ex)