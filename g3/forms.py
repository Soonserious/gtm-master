from django.forms.models import ModelForm
from .models import TeeShot, ApproachShot, FiftyFourShot, SeveGame, NineHole, HoganGame, ScoringGame
from main.models import Member
from django import forms


class TeeShotForm(ModelForm):
    class Meta:
        model = TeeShot
        fields = ['date'] + ['shot_{}'.format(shot_num + 1) for shot_num in range(14)]


class ApproachShotForm(ModelForm):
    class Meta:
        model = ApproachShot
        fields = ['date'] + ['shot_{}'.format(shot_num + 1) for shot_num in range(14)]


class FiftyFourShotForm(ModelForm):
    class Meta:
        model = FiftyFourShot
        fields = ['date'] + \
                 ['shot_1_1_{}'.format(shot_num + 1) for shot_num in range(5)] + \
                 ['shot_2_{}_{}'.format(shot_num1 + 1, shot_num2 + 1) for shot_num1 in range(5) for shot_num2 in
                  range(5)] + \
                 ['shot_3_1_{}'.format(shot_num + 1) for shot_num in range(5)] + \
                 ['shot_4_1_{}'.format(shot_num + 1) for shot_num in range(6)] + \
                 ['shot_5_1_{}'.format(shot_num + 1) for shot_num in range(3)] + \
                 ['shot_6_1_{}'.format(shot_num + 1) for shot_num in range(5)] + \
                 ['shot_7_1_{}'.format(shot_num + 1) for shot_num in range(5)]


class SeveGameForm(ModelForm):
    class Meta:
        model = SeveGame
        fields = ['date'] + \
                 ['shot_{}_{}'.format(shot_num1 + 1, shot_num2 + 1) for shot_num1 in range(4) for shot_num2 in
                  range(4)] + \
                 ['shot_5_1'] + \
                 ['shot_6_1']


class NineHoleForm(ModelForm):
    class Meta:
        model = NineHole
        fields = ['date'] + ['shot_{}'.format(shot_num + 1) for shot_num in range(9)]


class HoganGameForm(ModelForm):
    class Meta:
        model = HoganGame
        fields = ['date'] + \
                 ['shot_{}_{}'.format(shot_num1 + 1, shot_num2 + 1) for shot_num1 in range(3) for shot_num2 in range(6)]


class ScoringGameForm(ModelForm):
    class Meta:
        model = ScoringGame
        fields = ['date'] + \
                 ['shot_1_{}_{}_{}'.format(shot_num1 + 1, shot_num2 + 1, shot_num3 + 1) for shot_num1 in range(4) for
                  shot_num2 in range(3) for shot_num3 in range(3)] + \
                 ['shot_2_1_{}_{}'.format(shot_num1 + 1, shot_num2 + 1) for shot_num1 in range(5) for shot_num2 in
                  range(3)] + \
                 ['shot_3_1_{}_{}'.format(shot_num1 + 1, shot_num2 + 1) for shot_num1 in range(5) for shot_num2 in
                  range(3)] + \
                 ['shot_4_1_{}_1'.format(shot_num + 1) for shot_num in range(5)]


class MemberChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s%s(%s)" % (obj.user.last_name, obj.user.first_name, obj.user.username)


class MemberSelectForm(forms.Form):
    member = MemberChoiceField(queryset=Member.objects.all())
