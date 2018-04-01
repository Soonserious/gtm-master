# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json
import operator


class Criteria(models.Model):
    score = models.FloatField(default=71.2)
    fairway_hit = models.FloatField(default=62.80)
    gir = models.FloatField(default=64.90)
    putt = models.FloatField(default=29.18)
    putt_gir = models.FloatField(default=1.8)
    up_and_down = models.FloatField(default=60)
    bunker = models.FloatField(default=3)
    sand_save = models.FloatField(default=47)
    proximity = models.FloatField(default=7.00)
    birdie = models.FloatField(default=4)
    bogey = models.FloatField(default=4)
    double_bogey_or_more = models.FloatField(default=4)
    bounce_back = models.FloatField(default=60)
    penalty = models.FloatField(default=1)
    driving_distance = models.FloatField(default=288.6)


class GolfField(models.Model):
    TYPE = ((0, 'All'),  # 아마 안쓰일 것
            (1, 'Resort'),
            (2, 'Public'),
            (3, 'Private'))

    name = models.CharField(max_length=30, unique=True)
    type = models.SmallIntegerField(choices=TYPE)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    TYPE = ((0, 'Red'),  # 아마 안쓰일 것
            (1, 'White'),
            (2, 'Blue'),
            (3, 'Black'))

    field = models.ForeignKey(GolfField, on_delete=models.CASCADE)
    tee_type = models.SmallIntegerField(choices=TYPE)
    course_rating = models.IntegerField()
    slope_rating = models.IntegerField()

    hole_name_0 = models.CharField(max_length=50)
    hole_name_1 = models.CharField(max_length=50)

    yards = models.CharField(max_length=200)  # saved as [13,24,54,64,...,15]
    pars = models.CharField(max_length=200)
    handicaps = models.CharField(max_length=200)

    class Meta:
        unique_together = ('field', 'tee_type')

    def setyards(self, x):
        self.yards = json.dumps(x)

    def setpars(self, x):
        self.pars = json.dumps(x)

    def sethandicaps(self, x):
        self.handicaps = json.dumps(x)

    def getyards(self):
        return json.loads(self.yards)

    def getpars(self):
        return json.loads(self.pars)

    def gethandicaps(self):
        return json.loads(self.handicaps)

    def get_out_yards(self):
        return sum(self.getyards()[0:9])

    def get_in_yards(self):
        return sum(self.getyards()[9:18])

    def get_out_par(self):
        return sum(self.getpars()[0:9])

    def get_in_par(self):
        return sum(self.getpars()[9:18])

    def get_out_handicaps(self):
        return sum(self.gethandicaps()[0:9])

    def get_in_handicaps(self):
        return sum(self.gethandicaps()[9:18])

    def get_total_yards(self):
        return sum(self.getyards()[0:18])

    def get_total_par(self):
        return sum(self.getpars()[0:18])

    def get_total_handicaps(self):
        return sum(self.gethandicaps()[0:18])


class RoundingResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.datetime.today)
    create_time = models.DateTimeField(default=timezone.now)

    score = models.CharField(max_length=200)
    driving_distance = models.CharField(max_length=300)
    fairway_hit = models.CharField(max_length=200)
    putt = models.CharField(max_length=200)
    bunker = models.CharField(max_length=200)
    penalty = models.CharField(max_length=200)
    proximity = models.CharField(max_length=200)
    comment = models.TextField(default='', blank=True)

    def setscore(self, x):              self.score = json.dumps(x)

    def setdriving_distance(self, x):
        x = [0 if element is None else element for element in x]
        self.driving_distance = json.dumps(x)

    def setfairway_hit(self, x):         self.fairway_hit = json.dumps(x)

    def setputt(self, x):                self.putt = json.dumps(x)

    def setbunker(self, x):              self.bunker = json.dumps(x)

    def setpenalty(self, x):
        x = [0 if element is None else element for element in x]
        self.penalty = json.dumps(x)

    def setproximity(self, x):
        x = [0 if element is None else element for element in x]
        self.proximity = json.dumps(x)

    def getscore(self): return json.loads(self.score)

    def getdriving_distance(self): return json.loads(self.driving_distance)

    def getfairway_hit(self):
        return json.loads(self.fairway_hit)

    def getputt(self):
        return json.loads(self.putt)

    def getbunker(self):
        return json.loads(self.bunker)

    def getpenalty(self):
        return json.loads(self.penalty)

    def getproximity(self):
        return json.loads(self.proximity)

    def gir(self):
        return list(map(operator.le,
                        list(map(operator.sub, self.getscore(), self.getputt())),
                        list(map(operator.sub, self.course.getpars(), [2] * len(self.course.getpars())))))

    def putt_gir(self):
        return list(map(operator.mul, self.gir(), self.getputt()))

    def up_and_down(self):
        return list(map(operator.mul,
                   list(map(operator.not_, self.gir())),
                   list(map(operator.le, self.getscore(), self.course.getpars()))
                   ))

    def sand_save(self):
        return list(map(operator.mul, self.getbunker(),
                        list(map(operator.le, self.getputt(), [1] * len(self.getputt())))))

    def birdie(self):
        return list(map(operator.lt, self.getscore(), self.course.getpars()))

    def bogey(self):
        return list(map(operator.eq, self.getscore(), [par + 1 for par in self.course.getpars()]))

    def bogey_or_more(self):
        return list(map(operator.ge, self.getscore(), [par + 1 for par in self.course.getpars()]))

    def double_bogey(self):
        return list(map(operator.eq, self.getscore(), [par + 2 for par in self.course.getpars()]))

    def double_bogey_or_more(self):
        return list(map(operator.ge, self.getscore(), [par + 2 for par in self.course.getpars()]))

    def bounce_back(self):
        return list(map(operator.and_, [False] + self.bogey_or_more(), self.birdie() + [False]))[0:-1]

    def get_stat(self):
        par4 = list(map(operator.ge, self.course.getpars(), [4] * len(self.course.getpars())))
        driving_distance = list(map(operator.mul, self.getdriving_distance(), par4))
        fairway_hit = list(map(operator.mul, self.getfairway_hit(), par4))

        par4_in_cnt = sum(par4[:9])
        par4_out_cnt = sum(par4[9:])
        par4_cnt = par4_in_cnt + par4_out_cnt

        return {
            'out_score': sum(self.getscore()[0:9]),
            'in_score': sum(self.getscore()[9:18]),
            'score': sum(self.getscore()),
            'out_driving_distance': sum(driving_distance[0:9]) / par4_in_cnt if par4_in_cnt != 0 else 0,
            'in_driving_distance': sum(driving_distance[9:18]) / par4_out_cnt if par4_out_cnt != 0 else 0,
            'driving_distance': sum(driving_distance) / par4_cnt if par4_cnt != 0 else 0,
            'out_fairway_hit': sum(fairway_hit[0:9]) * 100.0 / par4_in_cnt if par4_in_cnt != 0 else 0,
            'in_fairway_hit': sum(fairway_hit[9:18]) * 100.0 / par4_out_cnt if par4_out_cnt != 0 else 0,
            'fairway_hit': sum(fairway_hit) * 100.0 / par4_cnt if par4_cnt != 0 else 0,
            'out_putt': sum(self.getputt()[0:9]),
            'in_putt': sum(self.getputt()[9:18]),
            'putt': sum(self.getputt()),
            'out_bunker': sum(self.getbunker()[0:9]),
            'in_bunker': sum(self.getbunker()[9:18]),
            'bunker': sum(self.getbunker()),
            'out_penalty': sum(self.getpenalty()[0:9]),
            'in_penalty': sum(self.getpenalty()[9:18]),
            'penalty': sum(self.getpenalty()),
            'out_proximity': sum(self.getproximity()[0:9]) / 9.0,
            'in_proximity': sum(self.getproximity()[9:18]) / 9.0,
            'proximity': sum(self.getproximity()) / 18.0,
            'out_gir': sum(self.gir()[0:9]),
            'in_gir': sum(self.gir()[9:18]),
            'gir': sum(self.gir()),
            'out_putt_gir': sum(self.putt_gir()[0:9]),
            'in_putt_gir': sum(self.putt_gir()[9:18]),
            'putt_gir': sum(self.putt_gir()),
            'out_up_and_down': sum(self.up_and_down()[0:9]),
            'in_up_and_down': sum(self.up_and_down()[9:18]),
            'up_and_down': sum(self.up_and_down()),
            'out_sand_save': sum(self.sand_save()[0:9]),
            'in_sand_save': sum(self.sand_save()[9:18]),
            'sand_save': sum(self.sand_save()),
            'out_birdie': sum(self.birdie()[0:9]),
            'in_birdie': sum(self.birdie()[9:18]),
            'birdie': sum(self.birdie()),
            'bogey': sum(self.bogey()),
            'bogey_or_more': sum(self.bogey_or_more()),
            'double_bogey_or_more': sum(self.double_bogey_or_more()),
            'out_bounce_back': sum(self.bounce_back()[0:9]),
            'in_bounce_back': sum(self.bounce_back()[9:18]),
            'bounce_back': sum(self.bounce_back()),
        }

class AVG_Stroke(models.Model):
    birdie = models.FloatField()
    par = models.FloatField()
    bogey = models.FloatField()
    double = models.FloatField()


