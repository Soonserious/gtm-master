# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import ModelForm
from .models import *


class CriteriaForm(ModelForm):
    class Meta:
        model = Criteria
        fields = ['score', 'fairway_hit', 'gir', 'putt', 'putt_gir',
                  'up_and_down', 'bunker', 'sand_save', 'proximity', 'birdie',  'bogey', 'double_bogey_or_more',
                  'bounce_back', 'penalty', 'driving_distance', 'Par', 'par3', 'par4', 'par5']


class GolfFieldForm(ModelForm):
    class Meta:
        model = GolfField
        fields = ['name', 'type', 'phone_number', 'address']
        labels = {
            'name': u'골프장 이름',
            'type': u'골프장 유형',
            'phone_number': u'전화번호',
            'address': u'골프장 주소',
        }
        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'temp_save'}),
            'phone_number' : forms.TextInput(attrs={'class' : 'temp_save'}),
            'address' : forms.TextInput(attrs={'class' : 'temp_save'}),
        }


class FindCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['field', 'tee_type']
        labels = {
            'tee_type': 'Tee',
        }


class CourseForm(ModelForm):
    yard_01 = forms.IntegerField(required=False)
    yard_02 = forms.IntegerField(required=False)
    yard_03 = forms.IntegerField(required=False)
    yard_04 = forms.IntegerField(required=False)
    yard_05 = forms.IntegerField(required=False)
    yard_06 = forms.IntegerField(required=False)
    yard_07 = forms.IntegerField(required=False)
    yard_08 = forms.IntegerField(required=False)
    yard_09 = forms.IntegerField(required=False)
    yard_10 = forms.IntegerField(required=False)
    yard_11 = forms.IntegerField(required=False)
    yard_12 = forms.IntegerField(required=False)
    yard_13 = forms.IntegerField(required=False)
    yard_14 = forms.IntegerField(required=False)
    yard_15 = forms.IntegerField(required=False)
    yard_16 = forms.IntegerField(required=False)
    yard_17 = forms.IntegerField(required=False)
    yard_18 = forms.IntegerField(required=False)

    par_01 = forms.IntegerField()
    par_02 = forms.IntegerField()
    par_03 = forms.IntegerField()
    par_04 = forms.IntegerField()
    par_05 = forms.IntegerField()
    par_06 = forms.IntegerField()
    par_07 = forms.IntegerField()
    par_08 = forms.IntegerField()
    par_09 = forms.IntegerField()
    par_10 = forms.IntegerField()
    par_11 = forms.IntegerField()
    par_12 = forms.IntegerField()
    par_13 = forms.IntegerField()
    par_14 = forms.IntegerField()
    par_15 = forms.IntegerField()
    par_16 = forms.IntegerField()
    par_17 = forms.IntegerField()
    par_18 = forms.IntegerField()

    handicap_01 = forms.IntegerField(required=False)
    handicap_02 = forms.IntegerField(required=False)
    handicap_03 = forms.IntegerField(required=False)
    handicap_04 = forms.IntegerField(required=False)
    handicap_05 = forms.IntegerField(required=False)
    handicap_06 = forms.IntegerField(required=False)
    handicap_07 = forms.IntegerField(required=False)
    handicap_08 = forms.IntegerField(required=False)
    handicap_09 = forms.IntegerField(required=False)
    handicap_10 = forms.IntegerField(required=False)
    handicap_11 = forms.IntegerField(required=False)
    handicap_12 = forms.IntegerField(required=False)
    handicap_13 = forms.IntegerField(required=False)
    handicap_14 = forms.IntegerField(required=False)
    handicap_15 = forms.IntegerField(required=False)
    handicap_16 = forms.IntegerField(required=False)
    handicap_17 = forms.IntegerField(required=False)
    handicap_18 = forms.IntegerField(required=False)

    hole_name_0 = forms.CharField()
    hole_name_1 = forms.CharField()

    class Meta:
        model = Course
        fields = ['course_rating', 'slope_rating', 'hole_name_0', 'hole_name_1']
        labels = {
            'course_rating': 'Course Rating',
            'slope_rating': 'Slope Rating',
        }

    def field_yards(self):
        return [self['yard_%02d' % x] for x in range(1, 19)]

    def field_pars(self):
        return [self['par_%02d' % x] for x in range(1, 19)]

    def field_handicaps(self):
        return [self['handicap_%02d' % x] for x in range(1, 19)]

    def yards(self):
        return [self.cleaned_data['yard_%02d' % x] for x in range(1, 19)]

    def pars(self):
        return [self.cleaned_data['par_%02d' % x] for x in range(1, 19)]

    def handicaps(self):
        return [self.cleaned_data['handicap_%02d' % x] for x in range(1, 19)]


class RoundingResultForm(ModelForm):
    date = forms.DateInput()

    score_01 = forms.IntegerField()
    score_02 = forms.IntegerField()
    score_03 = forms.IntegerField()
    score_04 = forms.IntegerField()
    score_05 = forms.IntegerField()
    score_06 = forms.IntegerField()
    score_07 = forms.IntegerField()
    score_08 = forms.IntegerField()
    score_09 = forms.IntegerField()
    score_10 = forms.IntegerField()
    score_11 = forms.IntegerField()
    score_12 = forms.IntegerField()
    score_13 = forms.IntegerField()
    score_14 = forms.IntegerField()
    score_15 = forms.IntegerField()
    score_16 = forms.IntegerField()
    score_17 = forms.IntegerField()
    score_18 = forms.IntegerField()

    driving_distance_01 = forms.IntegerField(required=False)
    driving_distance_02 = forms.IntegerField(required=False)
    driving_distance_03 = forms.IntegerField(required=False)
    driving_distance_04 = forms.IntegerField(required=False)
    driving_distance_05 = forms.IntegerField(required=False)
    driving_distance_06 = forms.IntegerField(required=False)
    driving_distance_07 = forms.IntegerField(required=False)
    driving_distance_08 = forms.IntegerField(required=False)
    driving_distance_09 = forms.IntegerField(required=False)
    driving_distance_10 = forms.IntegerField(required=False)
    driving_distance_11 = forms.IntegerField(required=False)
    driving_distance_12 = forms.IntegerField(required=False)
    driving_distance_13 = forms.IntegerField(required=False)
    driving_distance_14 = forms.IntegerField(required=False)
    driving_distance_15 = forms.IntegerField(required=False)
    driving_distance_16 = forms.IntegerField(required=False)
    driving_distance_17 = forms.IntegerField(required=False)
    driving_distance_18 = forms.IntegerField(required=False)

    fairway_hit_01 = forms.BooleanField(initial=False, required=False)
    fairway_hit_02 = forms.BooleanField(initial=False, required=False)
    fairway_hit_03 = forms.BooleanField(initial=False, required=False)
    fairway_hit_04 = forms.BooleanField(initial=False, required=False)
    fairway_hit_05 = forms.BooleanField(initial=False, required=False)
    fairway_hit_06 = forms.BooleanField(initial=False, required=False)
    fairway_hit_07 = forms.BooleanField(initial=False, required=False)
    fairway_hit_08 = forms.BooleanField(initial=False, required=False)
    fairway_hit_09 = forms.BooleanField(initial=False, required=False)
    fairway_hit_10 = forms.BooleanField(initial=False, required=False)
    fairway_hit_11 = forms.BooleanField(initial=False, required=False)
    fairway_hit_12 = forms.BooleanField(initial=False, required=False)
    fairway_hit_13 = forms.BooleanField(initial=False, required=False)
    fairway_hit_14 = forms.BooleanField(initial=False, required=False)
    fairway_hit_15 = forms.BooleanField(initial=False, required=False)
    fairway_hit_16 = forms.BooleanField(initial=False, required=False)
    fairway_hit_17 = forms.BooleanField(initial=False, required=False)
    fairway_hit_18 = forms.BooleanField(initial=False, required=False)

    putt_01 = forms.IntegerField()
    putt_02 = forms.IntegerField()
    putt_03 = forms.IntegerField()
    putt_04 = forms.IntegerField()
    putt_05 = forms.IntegerField()
    putt_06 = forms.IntegerField()
    putt_07 = forms.IntegerField()
    putt_08 = forms.IntegerField()
    putt_09 = forms.IntegerField()
    putt_10 = forms.IntegerField()
    putt_11 = forms.IntegerField()
    putt_12 = forms.IntegerField()
    putt_13 = forms.IntegerField()
    putt_14 = forms.IntegerField()
    putt_15 = forms.IntegerField()
    putt_16 = forms.IntegerField()
    putt_17 = forms.IntegerField()
    putt_18 = forms.IntegerField()

    bunker_01 = forms.BooleanField(initial=False, required=False)
    bunker_02 = forms.BooleanField(initial=False, required=False)
    bunker_03 = forms.BooleanField(initial=False, required=False)
    bunker_04 = forms.BooleanField(initial=False, required=False)
    bunker_05 = forms.BooleanField(initial=False, required=False)
    bunker_06 = forms.BooleanField(initial=False, required=False)
    bunker_07 = forms.BooleanField(initial=False, required=False)
    bunker_08 = forms.BooleanField(initial=False, required=False)
    bunker_09 = forms.BooleanField(initial=False, required=False)
    bunker_10 = forms.BooleanField(initial=False, required=False)
    bunker_11 = forms.BooleanField(initial=False, required=False)
    bunker_12 = forms.BooleanField(initial=False, required=False)
    bunker_13 = forms.BooleanField(initial=False, required=False)
    bunker_14 = forms.BooleanField(initial=False, required=False)
    bunker_15 = forms.BooleanField(initial=False, required=False)
    bunker_16 = forms.BooleanField(initial=False, required=False)
    bunker_17 = forms.BooleanField(initial=False, required=False)
    bunker_18 = forms.BooleanField(initial=False, required=False)

    penalty_01 = forms.IntegerField(required=False)
    penalty_02 = forms.IntegerField(required=False)
    penalty_03 = forms.IntegerField(required=False)
    penalty_04 = forms.IntegerField(required=False)
    penalty_05 = forms.IntegerField(required=False)
    penalty_06 = forms.IntegerField(required=False)
    penalty_07 = forms.IntegerField(required=False)
    penalty_08 = forms.IntegerField(required=False)
    penalty_09 = forms.IntegerField(required=False)
    penalty_10 = forms.IntegerField(required=False)
    penalty_11 = forms.IntegerField(required=False)
    penalty_12 = forms.IntegerField(required=False)
    penalty_13 = forms.IntegerField(required=False)
    penalty_14 = forms.IntegerField(required=False)
    penalty_15 = forms.IntegerField(required=False)
    penalty_16 = forms.IntegerField(required=False)
    penalty_17 = forms.IntegerField(required=False)
    penalty_18 = forms.IntegerField(required=False)

    proximity_01 = forms.IntegerField(required=False)
    proximity_02 = forms.IntegerField(required=False)
    proximity_03 = forms.IntegerField(required=False)
    proximity_04 = forms.IntegerField(required=False)
    proximity_05 = forms.IntegerField(required=False)
    proximity_06 = forms.IntegerField(required=False)
    proximity_07 = forms.IntegerField(required=False)
    proximity_08 = forms.IntegerField(required=False)
    proximity_09 = forms.IntegerField(required=False)
    proximity_10 = forms.IntegerField(required=False)
    proximity_11 = forms.IntegerField(required=False)
    proximity_12 = forms.IntegerField(required=False)
    proximity_13 = forms.IntegerField(required=False)
    proximity_14 = forms.IntegerField(required=False)
    proximity_15 = forms.IntegerField(required=False)
    proximity_16 = forms.IntegerField(required=False)
    proximity_17 = forms.IntegerField(required=False)
    proximity_18 = forms.IntegerField(required=False)
    course_id = forms.IntegerField()
    class Meta:
        model = RoundingResult
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker', 'required': 'True'}),
        }

    def field_score(self):
        return [self['score_%02d' % x] for x in range(1, 19)]

    def field_driving_distance(self):
        return [self['driving_distance_%02d' % x] for x in range(1, 19)]

    def field_fairway_hit(self):
        return [self['fairway_hit_%02d' % x] for x in range(1, 19)]

    def field_putt(self):
        return [self['putt_%02d' % x] for x in range(1, 19)]

    def field_bunker(self):
        return [self['bunker_%02d' % x] for x in range(1, 19)]

    def field_penalty(self):
        return [self['penalty_%02d' % x] for x in range(1, 19)]

    def field_proximity(self):
        return [self['proximity_%02d' % x] for x in range(1, 19)]

    def score(self):
        return [self.cleaned_data['score_%02d' % x] for x in range(1, 19)]

    def driving_distance(self):
        return [self.cleaned_data['driving_distance_%02d' % x] for x in range(1, 19)]

    def fairway_hit(self):
        return [self.cleaned_data['fairway_hit_%02d' % x] for x in range(1, 19)]

    def putt(self):
        return [self.cleaned_data['putt_%02d' % x] for x in range(1, 19)]

    def bunker(self):
        return [self.cleaned_data['bunker_%02d' % x] for x in range(1, 19)]

    def penalty(self):
        return [self.cleaned_data['penalty_%02d' % x] for x in range(1, 19)]

    def proximity(self):
        return [self.cleaned_data['proximity_%02d' % x] for x in range(1, 19)]