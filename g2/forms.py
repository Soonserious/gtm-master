from django.forms.models import ModelForm
from .models import GolfSwing, ShortGame, Putting


class GolfSwingForm(ModelForm):
    class Meta:
        model = GolfSwing
        fields = []


class ShortGameForm(ModelForm):
    class Meta:
        model = ShortGame
        fields = []


class PuttingForm(ModelForm):
    class Meta:
        model = Putting
        fields = []