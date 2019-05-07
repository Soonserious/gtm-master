from django.forms.models import ModelForm
from .models import PreshotRoutine, Diary, LongTermGoals, DailyGoals


class PreshotRoutineForm(ModelForm):
    class Meta:
        model = PreshotRoutine
        fields = []


class DiaryForm(ModelForm):
    class Meta:
        model = Diary
        fields = ['date', 'competition_level', 'competition_name','dumped_contents']


class LongTermGoalsForm(ModelForm):
    class Meta:
        model = LongTermGoals
        fields = []


class DailyGoalsForm(ModelForm):
    class Meta:
        model = DailyGoals
        fields = []