#-*- coding:utf-8 -*-
from django.forms.models import ModelForm
from .models import OceanTest, Gmet, Tops, Fss, Acsi, CourseManagement


class OceanTestForm(ModelForm):
    class Meta:
        model = OceanTest
        fields = ['sex']
        labels = {'sex': u'성별'}

class GmetForm(ModelForm):
    class Meta:
        model = Gmet
        fields = ['sex']
        labels = {'sex': u'성별'}

class TopsForm(ModelForm):
    class Meta:
        model = Tops
        fields = []

class TopsCommentForm(ModelForm):
    class Meta:
        model = Tops
        fields = []

class FssForm(ModelForm):
    class Meta:
        model = Fss
        fields = []

class AcsiForm(ModelForm):
    class Meta:
        model = Acsi
        fields = []

class CourseManagementForm(ModelForm):
    class Meta:
        model = CourseManagement
        fields = []

class CourseManagementCommentForm(ModelForm):
    class Meta:
        model = CourseManagement
        fields = []
