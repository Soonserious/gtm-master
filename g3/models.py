from django.db import models
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User


class TeeShot(models.Model):
    # user_id = models.CharField('user_id', max_length=30)  # TODO : Change this to Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField('date', blank=False)
    create_time = models.DateTimeField(default=timezone.now)

    shot_1 = models.IntegerField(blank=False)
    shot_2 = models.IntegerField(blank=False)
    shot_3 = models.IntegerField(blank=False)
    shot_4 = models.IntegerField(blank=False)
    shot_5 = models.IntegerField(blank=False)
    shot_6 = models.IntegerField(blank=False)
    shot_7 = models.IntegerField(blank=False)
    shot_8 = models.IntegerField(blank=False)
    shot_9 = models.IntegerField(blank=False)
    shot_10 = models.IntegerField(blank=False)
    shot_11 = models.IntegerField(blank=False)
    shot_12 = models.IntegerField(blank=False)
    shot_13 = models.IntegerField(blank=False)
    shot_14 = models.IntegerField(blank=False)

    @staticmethod
    def get_level_by_score(score):
        if score >= 18:
            level = 5
        elif score >= 15:
            level = 4
        elif score >= 12:
            level = 3
        elif score >= 9:
            level = 2
        elif score >= 6:
            level = 1
        else:
            level = 0
        return level

    def result_non_json(self):
        score = 0
        for field in self._meta.get_fields():
            field_name = field.name
            if field_name.startswith("shot"):
                score += getattr(self, field_name, None)
        level = self.get_level_by_score(score)

        return {'score': score, 'level': level, 'date': self.date}

    def result(self):
        score = 0
        for field in self._meta.get_fields():
            field_name = field.name
            if field_name.startswith("shot"):
                score += getattr(self, field_name, None)
        level = self.get_level_by_score(score)

        return JsonResponse({'score': score, 'level': level})


class ApproachShot(models.Model):
    # user_id = models.CharField('user_id', max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField('date', blank=False)
    create_time = models.DateTimeField(default=timezone.now)

    shot_1 = models.IntegerField(blank=False)
    shot_2 = models.IntegerField(blank=False)
    shot_3 = models.IntegerField(blank=False)
    shot_4 = models.IntegerField(blank=False)
    shot_5 = models.IntegerField(blank=False)
    shot_6 = models.IntegerField(blank=False)
    shot_7 = models.IntegerField(blank=False)
    shot_8 = models.IntegerField(blank=False)
    shot_9 = models.IntegerField(blank=False)
    shot_10 = models.IntegerField(blank=False)
    shot_11 = models.IntegerField(blank=False)
    shot_12 = models.IntegerField(blank=False)
    shot_13 = models.IntegerField(blank=False)
    shot_14 = models.IntegerField(blank=False)

    @staticmethod
    def get_level_by_score(score):
        if score >= 18:
            level = 5
        elif score >= 15:
            level = 4
        elif score >= 12:
            level = 3
        elif score >= 9:
            level = 2
        elif score >= 6:
            level = 1
        else:
            level = 0
        return level

    def result_non_json(self):
        score = 0
        for field in self._meta.get_fields():
            field_name = field.name
            if field_name.startswith("shot"):
                score += getattr(self, field_name, None)
        level = self.get_level_by_score(score)

        return {'score': score, 'level': level, 'date': self.date}

    # TODO : Not a good idea make a json object in model.
    def result(self):
        score = 0
        for field in self._meta.get_fields():
            field_name = field.name
            if field_name.startswith("shot"):
                score += getattr(self, field_name, None)
        level = self.get_level_by_score(score)

        return JsonResponse({'score': score, 'level': level})


class FiftyFourShot(models.Model):
    # user_id = models.CharField('user_id', max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField('date', blank=False)
    create_time = models.DateTimeField(default=timezone.now)

    shot_1_1_1 = models.IntegerField(blank=False)
    shot_1_1_2 = models.IntegerField(blank=False)
    shot_1_1_3 = models.IntegerField(blank=False)
    shot_1_1_4 = models.IntegerField(blank=False)
    shot_1_1_5 = models.IntegerField(blank=False)

    shot_2_1_1 = models.IntegerField(blank=False)
    shot_2_1_2 = models.IntegerField(blank=False)
    shot_2_1_3 = models.IntegerField(blank=False)
    shot_2_1_4 = models.IntegerField(blank=False)
    shot_2_1_5 = models.IntegerField(blank=False)

    shot_2_2_1 = models.IntegerField(blank=False)
    shot_2_2_2 = models.IntegerField(blank=False)
    shot_2_2_3 = models.IntegerField(blank=False)
    shot_2_2_4 = models.IntegerField(blank=False)
    shot_2_2_5 = models.IntegerField(blank=False)

    shot_2_3_1 = models.IntegerField(blank=False)
    shot_2_3_2 = models.IntegerField(blank=False)
    shot_2_3_3 = models.IntegerField(blank=False)
    shot_2_3_4 = models.IntegerField(blank=False)
    shot_2_3_5 = models.IntegerField(blank=False)

    shot_2_4_1 = models.IntegerField(blank=False)
    shot_2_4_2 = models.IntegerField(blank=False)
    shot_2_4_3 = models.IntegerField(blank=False)
    shot_2_4_4 = models.IntegerField(blank=False)
    shot_2_4_5 = models.IntegerField(blank=False)

    shot_2_5_1 = models.IntegerField(blank=False)
    shot_2_5_2 = models.IntegerField(blank=False)
    shot_2_5_3 = models.IntegerField(blank=False)
    shot_2_5_4 = models.IntegerField(blank=False)
    shot_2_5_5 = models.IntegerField(blank=False)

    shot_3_1_1 = models.IntegerField(blank=False)
    shot_3_1_2 = models.IntegerField(blank=False)
    shot_3_1_3 = models.IntegerField(blank=False)
    shot_3_1_4 = models.IntegerField(blank=False)
    shot_3_1_5 = models.IntegerField(blank=False)

    shot_4_1_1 = models.IntegerField(blank=False)
    shot_4_1_2 = models.IntegerField(blank=False)
    shot_4_1_3 = models.IntegerField(blank=False)
    shot_4_1_4 = models.IntegerField(blank=False)
    shot_4_1_5 = models.IntegerField(blank=False)
    shot_4_1_6 = models.IntegerField(blank=False)

    shot_5_1_1 = models.IntegerField(blank=False)
    shot_5_1_2 = models.IntegerField(blank=False)
    shot_5_1_3 = models.IntegerField(blank=False)

    shot_6_1_1 = models.IntegerField(blank=False)
    shot_6_1_2 = models.IntegerField(blank=False)
    shot_6_1_3 = models.IntegerField(blank=False)
    shot_6_1_4 = models.IntegerField(blank=False)
    shot_6_1_5 = models.IntegerField(blank=False)

    shot_7_1_1 = models.IntegerField(blank=False)
    shot_7_1_2 = models.IntegerField(blank=False)
    shot_7_1_3 = models.IntegerField(blank=False)
    shot_7_1_4 = models.IntegerField(blank=False)
    shot_7_1_5 = models.IntegerField(blank=False)

    @staticmethod
    def get_level_by_score(score):
        if score >= 220:
            level = 5
        elif score >= 210:
            level = 4
        elif score >= 185:
            level = 3
        elif score >= 160:
            level = 2
        elif score >= 135:
            level = 1
        else:
            level = 0
        return level

    def result_non_json(self):
        score = 0
        for field in self._meta.get_fields():
            field_name = field.name
            if field_name.startswith("shot"):
                score += getattr(self, field_name, None)
        level = self.get_level_by_score(score)

        return {'score': score, 'level': level, 'date': self.date}

    def result(self):
        score = 0
        for field in self._meta.get_fields():
            field_name = field.name
            if field_name.startswith("shot"):
                score += getattr(self, field_name, None)
        level = self.get_level_by_score(score)

        return JsonResponse({'score': score, 'level': level})


class SeveGame(models.Model):
    # user_id = models.CharField('user_id', max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField('date', blank=False)
    create_time = models.DateTimeField(default=timezone.now)

    shot_1_1 = models.SmallIntegerField(blank=False)
    shot_1_2 = models.SmallIntegerField(blank=False)
    shot_1_3 = models.SmallIntegerField(blank=False)
    shot_1_4 = models.SmallIntegerField(blank=False)

    shot_2_1 = models.SmallIntegerField(blank=False)
    shot_2_2 = models.SmallIntegerField(blank=False)
    shot_2_3 = models.SmallIntegerField(blank=False)
    shot_2_4 = models.SmallIntegerField(blank=False)

    shot_3_1 = models.SmallIntegerField(blank=False)
    shot_3_2 = models.SmallIntegerField(blank=False)
    shot_3_3 = models.SmallIntegerField(blank=False)
    shot_3_4 = models.SmallIntegerField(blank=False)

    shot_4_1 = models.SmallIntegerField(blank=False)
    shot_4_2 = models.SmallIntegerField(blank=False)
    shot_4_3 = models.SmallIntegerField(blank=False)
    shot_4_4 = models.SmallIntegerField(blank=False)

    shot_5_1 = models.SmallIntegerField(blank=False)

    shot_6_1 = models.SmallIntegerField(blank=False)

    @staticmethod
    def get_level_by_score(score):
        if score <= 76:
            level = 5
        elif score <= 79:
            level = 4
        elif score <= 82:
            level = 3
        elif score <= 85:
            level = 2
        elif score <= 88:
            level = 1
        else:
            level = 0
        return level

    def result_non_json(self):
        score = 0
        for field in self._meta.get_fields():
            field_name = field.name
            if field_name.startswith("shot"):
                score += getattr(self, field_name, None)
        level = self.get_level_by_score(score)

        return {'score': score, 'level': level, 'date': self.date}

    def result(self):
        score = 0
        for field in self._meta.get_fields():
            field_name = field.name
            if field_name.startswith("shot"):
                score += getattr(self, field_name, None)
        level = self.get_level_by_score(score)

        return JsonResponse({'score': score, 'level': level})


class NineHole(models.Model):
    # user_id = models.CharField('user_id', max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField('date', blank=False)
    create_time = models.DateTimeField(default=timezone.now)

    shot_1 = models.SmallIntegerField(blank=False)
    shot_2 = models.SmallIntegerField(blank=False)
    shot_3 = models.SmallIntegerField(blank=False)
    shot_4 = models.SmallIntegerField(blank=False)
    shot_5 = models.SmallIntegerField(blank=False)
    shot_6 = models.SmallIntegerField(blank=False)
    shot_7 = models.SmallIntegerField(blank=False)
    shot_8 = models.SmallIntegerField(blank=False)
    shot_9 = models.SmallIntegerField(blank=False)

    @staticmethod
    def get_level_by_score(score):
        if score <= 20:
            level = 5
        elif score <= 21:
            level = 4
        elif score <= 22:
            level = 3
        elif score <= 24:
            level = 2
        elif score <= 26:
            level = 1
        else:
            level = 0
        return level

    def result_non_json(self):
        score = 0
        for field in self._meta.get_fields():
            field_name = field.name
            if field_name.startswith("shot"):
                score += getattr(self, field_name, None)
        level = self.get_level_by_score(score)

        return {'score': score, 'level': level, 'date': self.date}

    def result(self):
        score = 0
        for field in self._meta.get_fields():
            field_name = field.name
            if field_name.startswith("shot"):
                score += getattr(self, field_name, None)
        level = self.get_level_by_score(score)

        return JsonResponse({'score': score, 'level': level})


class HoganGame(models.Model):
    # user_id = models.CharField('user_id', max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField('date', blank=False)
    create_time = models.DateTimeField(default=timezone.now)

    shot_1_1 = models.SmallIntegerField(blank=False)
    shot_1_2 = models.SmallIntegerField(blank=False)
    shot_1_3 = models.SmallIntegerField(blank=False)
    shot_1_4 = models.SmallIntegerField(blank=False)
    shot_1_5 = models.SmallIntegerField(blank=False)
    shot_1_6 = models.SmallIntegerField(blank=False)

    shot_2_1 = models.SmallIntegerField(blank=False)
    shot_2_2 = models.SmallIntegerField(blank=False)
    shot_2_3 = models.SmallIntegerField(blank=False)
    shot_2_4 = models.SmallIntegerField(blank=False)
    shot_2_5 = models.SmallIntegerField(blank=False)
    shot_2_6 = models.SmallIntegerField(blank=False)

    shot_3_1 = models.SmallIntegerField(blank=False)
    shot_3_2 = models.SmallIntegerField(blank=False)
    shot_3_3 = models.SmallIntegerField(blank=False)
    shot_3_4 = models.SmallIntegerField(blank=False)
    shot_3_5 = models.SmallIntegerField(blank=False)
    shot_3_6 = models.SmallIntegerField(blank=False)

    @staticmethod
    def get_level_by_score(score):
        if score <= 64:
            level = 5
        elif score <= 66:
            level = 4
        elif score <= 68:
            level = 3
        elif score <= 70:
            level = 2
        elif score <= 72:
            level = 1
        else:
            level = 0
        return level

    def result_non_json(self):
        score = 0
        for field in self._meta.get_fields():
            field_name = field.name
            if field_name.startswith("shot"):
                score += getattr(self, field_name, None)
        level = self.get_level_by_score(score)

        return {'score': score, 'level': level, 'date': self.date}

    def result(self):
        score = 0
        for field in self._meta.get_fields():
            field_name = field.name
            if field_name.startswith("shot"):
                score += getattr(self, field_name, None)
        level = self.get_level_by_score(score)

        return JsonResponse({'score': score, 'level': level})


class ScoringGame(models.Model):
    # user_id = models.CharField('user_id', max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField('date', blank=False)
    create_time = models.DateTimeField(default=timezone.now)

    shot_1_1_1_1 = models.IntegerField(blank=False)
    shot_1_1_1_2 = models.IntegerField(blank=False)
    shot_1_1_1_3 = models.IntegerField(blank=False)
    shot_1_1_2_1 = models.IntegerField(blank=False)
    shot_1_1_2_2 = models.IntegerField(blank=False)
    shot_1_1_2_3 = models.IntegerField(blank=False)
    shot_1_1_3_1 = models.IntegerField(blank=False)
    shot_1_1_3_2 = models.IntegerField(blank=False)
    shot_1_1_3_3 = models.IntegerField(blank=False)

    shot_1_2_1_1 = models.IntegerField(blank=False)
    shot_1_2_1_2 = models.IntegerField(blank=False)
    shot_1_2_1_3 = models.IntegerField(blank=False)
    shot_1_2_2_1 = models.IntegerField(blank=False)
    shot_1_2_2_2 = models.IntegerField(blank=False)
    shot_1_2_2_3 = models.IntegerField(blank=False)
    shot_1_2_3_1 = models.IntegerField(blank=False)
    shot_1_2_3_2 = models.IntegerField(blank=False)
    shot_1_2_3_3 = models.IntegerField(blank=False)

    shot_1_3_1_1 = models.IntegerField(blank=False)
    shot_1_3_1_2 = models.IntegerField(blank=False)
    shot_1_3_1_3 = models.IntegerField(blank=False)
    shot_1_3_2_1 = models.IntegerField(blank=False)
    shot_1_3_2_2 = models.IntegerField(blank=False)
    shot_1_3_2_3 = models.IntegerField(blank=False)
    shot_1_3_3_1 = models.IntegerField(blank=False)
    shot_1_3_3_2 = models.IntegerField(blank=False)
    shot_1_3_3_3 = models.IntegerField(blank=False)

    shot_1_4_1_1 = models.IntegerField(blank=False)
    shot_1_4_1_2 = models.IntegerField(blank=False)
    shot_1_4_1_3 = models.IntegerField(blank=False)
    shot_1_4_2_1 = models.IntegerField(blank=False)
    shot_1_4_2_2 = models.IntegerField(blank=False)
    shot_1_4_2_3 = models.IntegerField(blank=False)
    shot_1_4_3_1 = models.IntegerField(blank=False)
    shot_1_4_3_2 = models.IntegerField(blank=False)
    shot_1_4_3_3 = models.IntegerField(blank=False)

    shot_2_1_1_1 = models.IntegerField(blank=False)
    shot_2_1_1_2 = models.IntegerField(blank=False)
    shot_2_1_1_3 = models.IntegerField(blank=False)
    shot_2_1_2_1 = models.IntegerField(blank=False)
    shot_2_1_2_2 = models.IntegerField(blank=False)
    shot_2_1_2_3 = models.IntegerField(blank=False)
    shot_2_1_3_1 = models.IntegerField(blank=False)
    shot_2_1_3_2 = models.IntegerField(blank=False)
    shot_2_1_3_3 = models.IntegerField(blank=False)
    shot_2_1_4_1 = models.IntegerField(blank=False)
    shot_2_1_4_2 = models.IntegerField(blank=False)
    shot_2_1_4_3 = models.IntegerField(blank=False)
    shot_2_1_5_1 = models.IntegerField(blank=False)
    shot_2_1_5_2 = models.IntegerField(blank=False)
    shot_2_1_5_3 = models.IntegerField(blank=False)

    shot_3_1_1_1 = models.IntegerField(blank=False)
    shot_3_1_1_2 = models.IntegerField(blank=False)
    shot_3_1_1_3 = models.IntegerField(blank=False)
    shot_3_1_2_1 = models.IntegerField(blank=False)
    shot_3_1_2_2 = models.IntegerField(blank=False)
    shot_3_1_2_3 = models.IntegerField(blank=False)
    shot_3_1_3_1 = models.IntegerField(blank=False)
    shot_3_1_3_2 = models.IntegerField(blank=False)
    shot_3_1_3_3 = models.IntegerField(blank=False)
    shot_3_1_4_1 = models.IntegerField(blank=False)
    shot_3_1_4_2 = models.IntegerField(blank=False)
    shot_3_1_4_3 = models.IntegerField(blank=False)
    shot_3_1_5_1 = models.IntegerField(blank=False)
    shot_3_1_5_2 = models.IntegerField(blank=False)
    shot_3_1_5_3 = models.IntegerField(blank=False)

    shot_4_1_1_1 = models.IntegerField(blank=False)
    shot_4_1_2_1 = models.IntegerField(blank=False)
    shot_4_1_3_1 = models.IntegerField(blank=False)
    shot_4_1_4_1 = models.IntegerField(blank=False)
    shot_4_1_5_1 = models.IntegerField(blank=False)

    @staticmethod
    def get_level_by_score_short_putting(score):
        if score >= 22:
            level = 5
        elif score >= 20:
            level = 4
        elif score >= 18:
            level = 3
        elif score >= 15:
            level = 2
        elif score >= 12:
            level = 1
        else:
            level = 0
        return level

    @staticmethod
    def get_level_by_score_middle_putting(score):
        if score >= 17:
            level = 5
        elif score >= 16:
            level = 4
        elif score >= 14:
            level = 3
        elif score >= 12:
            level = 2
        elif score >= 9:
            level = 1
        else:
            level = 0
        return level

    @staticmethod
    def get_level_by_score_long_putting(score):
        if score >= 10:
            level = 5
        elif score >= 9:
            level = 4
        elif score >= 8:
            level = 3
        elif score >= 7:
            level = 2
        elif score >= 6:
            level = 1
        else:
            level = 0
        return level

    @staticmethod
    def get_level_by_score_chipping(score):
        if score >= 13:
            level = 5
        elif score >= 12:
            level = 4
        elif score >= 10:
            level = 3
        elif score >= 9:
            level = 2
        elif score >= 7:
            level = 1
        else:
            level = 0
        return level

    @staticmethod
    def get_level_by_score_pitching(score):
        if score >= 10:
            level = 5
        elif score >= 9:
            level = 4
        elif score >= 8:
            level = 3
        elif score >= 7:
            level = 2
        elif score >= 6:
            level = 1
        else:
            level = 0
        return level

    @staticmethod
    def get_level_by_score_bunker(score):
        if score >= 6:
            level = 5
        elif score >= 5:
            level = 4
        elif score >= 4:
            level = 3
        elif score >= 2:
            level = 2
        elif score >= 1:
            level = 1
        else:
            level = 0
        return level

    @staticmethod
    def get_level_by_score(score):
        if score >= 75:
            level = 5
        elif score >= 69:
            level = 4
        elif score >= 60:
            level = 3
        elif score >= 52:
            level = 2
        elif score >= 41:
            level = 1
        else:
            level = 0
        return level

    def result_non_json(self):
        short_putting_score = 0
        middle_putting_score = 0
        long_putting_score = 0
        chipping_score = 0
        pitching_score = 0
        bunker_score = 0

        for field in self._meta.get_fields():
            field_name = field.name
            if field_name.startswith("shot_1"):
                if field_name.endswith("1"):
                    short_putting_score += getattr(self, field_name, None)
                elif field_name.endswith("2"):
                    middle_putting_score += getattr(self, field_name, None)
                elif field_name.endswith("3"):
                    long_putting_score += getattr(self, field_name, None)
            elif field_name.startswith("shot_2"):
                chipping_score += getattr(self, field_name, None)
            elif field_name.startswith("shot_3"):
                pitching_score += getattr(self, field_name, None)
            elif field_name.startswith("shot_4"):
                bunker_score += getattr(self, field_name, None)

        short_putting_level = self.get_level_by_score_short_putting(short_putting_score)
        middle_putting_level = self.get_level_by_score_middle_putting(middle_putting_score)
        long_putting_level = self.get_level_by_score_long_putting(long_putting_score)
        chipping_level = self.get_level_by_score_chipping(chipping_score)
        pitching_level = self.get_level_by_score_pitching(pitching_score)
        bunker_level = self.get_level_by_score_bunker(bunker_score)

        score = short_putting_score + middle_putting_score + long_putting_score + chipping_score +\
            pitching_score + bunker_score

        level = self.get_level_by_score(score)

        return {'score': score,
                'level': level,
                'short_putting_score': short_putting_score, 'short_putting_level': short_putting_level,
                'middle_putting_score': middle_putting_score, 'middle_putting_level': middle_putting_level,
                'long_putting_score': long_putting_score, 'long_putting_level': long_putting_level,
                'chipping_score': chipping_score, 'chipping_level': chipping_level,
                'pitching_score': pitching_score, 'pitching_level': pitching_level,
                'bunker_score': bunker_score, 'bunker_level': bunker_level, 'date': self.date}

    def result(self):
        short_putting_score = 0
        middle_putting_score = 0
        long_putting_score = 0
        chipping_score = 0
        pitching_score = 0
        bunker_score = 0

        for field in self._meta.get_fields():
            field_name = field.name
            if field_name.startswith("shot_1"):
                if field_name.endswith("1"):
                    short_putting_score += getattr(self, field_name, None)
                elif field_name.endswith("2"):
                    middle_putting_score += getattr(self, field_name, None)
                elif field_name.endswith("3"):
                    long_putting_score += getattr(self, field_name, None)
            elif field_name.startswith("shot_2"):
                chipping_score += getattr(self, field_name, None)
            elif field_name.startswith("shot_3"):
                pitching_score += getattr(self, field_name, None)
            elif field_name.startswith("shot_4"):
                bunker_score += getattr(self, field_name, None)

        if short_putting_score >= 22:
            short_putting_level = 5
        elif short_putting_score >= 20:
            short_putting_level = 4
        elif short_putting_score >= 18:
            short_putting_level = 3
        elif short_putting_score >= 15:
            short_putting_level = 2
        elif short_putting_score >= 12:
            short_putting_level = 1
        else:
            short_putting_level = 0

        if middle_putting_score >= 17:
            middle_putting_level = 5
        elif middle_putting_score >= 16:
            middle_putting_level = 4
        elif middle_putting_score >= 14:
            middle_putting_level = 3
        elif middle_putting_score >= 12:
            middle_putting_level = 2
        elif middle_putting_score >= 9:
            middle_putting_level = 1
        else:
            middle_putting_level = 0

        if long_putting_score >= 10:
            long_putting_level = 5
        elif long_putting_score >= 9:
            long_putting_level = 4
        elif long_putting_score >= 8:
            long_putting_level = 3
        elif long_putting_score >= 7:
            long_putting_level = 2
        elif long_putting_score >= 6:
            long_putting_level = 1
        else:
            long_putting_level = 0

        if chipping_score >= 13:
            chipping_level = 5
        elif chipping_score >= 12:
            chipping_level = 4
        elif chipping_score >= 10:
            chipping_level = 3
        elif chipping_score >= 9:
            chipping_level = 2
        elif chipping_score >= 7:
            chipping_level = 1
        else:
            chipping_level = 0

        if pitching_score >= 10:
            pitching_level = 5
        elif pitching_score >= 9:
            pitching_level = 4
        elif pitching_score >= 8:
            pitching_level = 3
        elif pitching_score >= 7:
            pitching_level = 2
        elif pitching_score >= 6:
            pitching_level = 1
        else:
            pitching_level = 0

        if bunker_score >= 6:
            bunker_level = 5
        elif bunker_score >= 4:
            bunker_level = 3
        elif bunker_score >= 2:
            bunker_level = 1
        else:
            bunker_level = 0

        score = short_putting_score + middle_putting_score + long_putting_score + chipping_score + pitching_score + bunker_score

        if score >= 75:
            level = 5
        elif score >= 69:
            level = 4
        elif score >= 60:
            level = 3
        elif score >= 52:
            level = 2
        elif score >= 41:
            level = 1
        else:
            level = 0

        return JsonResponse({'score': score, 'level': level,
                             'short_putting_score': short_putting_score, 'short_putting_level': short_putting_level,
                             'middle_putting_score': middle_putting_score, 'middle_putting_level': middle_putting_level,
                             'long_putting_score': long_putting_score, 'long_putting_level': long_putting_level,
                             'chipping_score': chipping_score, 'chipping_level': chipping_level,
                             'pitching_score': pitching_score, 'pitching_level': pitching_level,
                             'bunker_score': bunker_score, 'bunker_level': bunker_level}
                            )


class PowerGameAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # teeshot = models.ForeignKey(TeeShot, on_delete=models.CASCADE)
    # approachshot = models.ForeignKey(ApproachShot, on_delete=models.CASCADE)
    # fiftyfourshot = models.ForeignKey(FiftyFourShot, on_delete=models.CASCADE)

    update_time = models.DateTimeField(default=timezone.now)
    comment = models.TextField(default='', blank=True)
    strategy = models.TextField(default='', blank=True)


class ScoringGameAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # sevegame = models.ForeignKey(SeveGame, on_delete=models.CASCADE)
    # ninehole = models.ForeignKey(NineHole, on_delete=models.CASCADE)
    # hogangame = models.ForeignKey(HoganGame, on_delete=models.CASCADE)
    # scoring = models.ForeignKey(ScoringGame, on_delete=models.CASCADE)

    update_time = models.DateTimeField(default=timezone.now)
    comment = models.TextField(default='', blank=True)
    strategy = models.TextField(default='', blank=True)