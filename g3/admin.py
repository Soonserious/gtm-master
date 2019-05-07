from django.contrib import admin
from g3.models import TeeShot, ApproachShot, FiftyFourShot, SeveGame, NineHole, HoganGame, ScoringGame


admin.site.register(TeeShot)
admin.site.register(ApproachShot)
admin.site.register(FiftyFourShot)

admin.site.register(SeveGame)
admin.site.register(NineHole)

admin.site.register(HoganGame)

admin.site.register(ScoringGame)
