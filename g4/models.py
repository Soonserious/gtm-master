#-*- coding:utf-8 -*-

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import numpy as np
import json
import pytz


def get_local_date(datetime):
    local_tz = pytz.timezone('Asia/Seoul')
    return datetime.astimezone(local_tz).strftime("%Y-%m-%d %a %I:%M %p")


class SurveyInfo:
    def __init__(self, choices, first_num, last_num):
        # score(answer to each question): integer in (score_domain)
        self.answer_choices = choices
        # question number: i, i+1, ..., j-1, j
        self.first_num = first_num  # i
        self.last_num = last_num  # j
        self.num_questions = last_num - first_num + 1
        # labels
        self.answer_labels = None
        self.question_labels = None

    def set_answer_labels(self, answer_labels):
        assert type(answer_labels) == list
        assert len(answer_labels) == len(self.answer_choices)
        self.answer_labels = answer_labels

    def set_question_labels(self, question_labels):
        assert type(question_labels) == list
        assert len(question_labels) == self.num_questions
        self.question_labels = question_labels


class OceanTest(models.Model):
    full_title = 'Ocean Test'

    survey_info = SurveyInfo(choices=[1, 2, 3, 4, 5, 6, 7], first_num=1, last_num=10)
    survey_info.set_answer_labels(['완전히 부정한다',
                                   '다소 부정한다',
                                   '약간 부정한다',
                                   '동의도 부정도 하지 않는다',
                                   '약간 동의한다',
                                   '다소 동의한다',
                                   '완전히 동의한다'])
    survey_info.set_question_labels(['외향적이며, 열정적이다.',
                                     '비판적이며, 화를 잘 낸다.',
                                     '믿을 만하며, 자기 관리를 잘한다.',
                                     '불안하며, 쉽게 마음이 상한다.',
                                     '새로운 경험에 개방적이다.',
                                     '속마음을 드러내지 않으며, 조용하다.',
                                     '동점심이 많으며, 따뜻하다.',
                                     '계획성이 없으며, 부주의하다.',
                                     '침착하며, 감정적으로 안정되어 있다.',
                                     '전통적이며, 창의성이 없다.'])
    result_labels = ['개방성',
                     '성실성',
                     '외향성',
                     '친화성',
                     '신경성']
    partition = [[5, 10],
                 [3, 8],
                 [1, 6],
                 [2, 7],
                 [4, 9]]
    reverse_scoring = [2, 6, 8, 9, 10]
    reverse_constant = 8
    avg_values = {'M': [10.7, 10.4, 8.5, 10.1, 5.7],
                  'F': [10.8, 11.0, 9.1, 10.6, 6.7]}
    stddev_values = {'M': [2.18, 2.30, 2.82, 2.20, 2.62],
                     'F': [2.12, 2.22, 2.94, 2.22, 2.90]}

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateTimeField(default=timezone.now)
    SEX_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='M')
    dumped_scores = models.CharField(max_length=survey_info.num_questions * 10, blank=True)
    comment = models.TextField(default='', blank=True)
    strategy = models.TextField(default='', blank=True)

    def get_results(self):
        loaded_scores = json.loads(getattr(self, 'dumped_scores'))
        for i in self.reverse_scoring:
            loaded_scores[str(i)] = self.reverse_constant - loaded_scores[str(i)]
        result_values = dict()
        result_values['score'] = [0 for _ in range(len(self.partition))]
        for i, div in enumerate(self.partition):
            for q_num in div:
                result_values['score'][i] += loaded_scores[str(q_num)]

        result_values['t-score'] = []
        for i, (avg, stddev) in enumerate(zip(self.avg_values[getattr(self, 'sex')],
                                              self.stddev_values[getattr(self, 'sex')])):
            result_values['t-score'].append(50.0 + (result_values['score'][i] - avg) / stddev * 10.0)

        for key in ['score', 't-score']:
            result_values[key] = [round(x, 2) for x in result_values[key]]

        return {'date': get_local_date(getattr(self, 'update_time')),
                'scores': result_values['score'],
                't-scores': result_values['t-score']}


class Gmet(models.Model):
    full_title = 'IZOF based GMET Profiling'

    survey_info = SurveyInfo(choices=[1, 2, 3, 4, 5], first_num=1, last_num=42)
    survey_info.set_answer_labels(['전혀 그렇지 않음 (1)',
                                   '그렇지 않음 (2)',
                                   '보통임 (3)',
                                   '약간 그러함 (4)',
                                   '매우 그러함 (5)'])
    survey_info.set_question_labels(['나는 샷을 준비할 때 마음이 산만해지고 주의집중이 되지 않는 경우가 있다.',
                                     '비가 오거나 바람이 심하게 부는 날씨에는 집중력을 유지하는 것이 어렵다.',
                                     '나는 실수를 하면 갤러리나 동반자를 의식하게 되고, 이로 인해 집중력이 흐트러지고 수행을 하기 힘들었던 적이 있다.',
                                     '나는 경기 중에 갤러리나 동반자의 말, 버릇, 습관, 태도 또는 동반자의 플레이에 민감하게 영향을 받는다.',
                                     '나는 경기 중에 자신의 플레이에 집중하기보다 동반자들에 대한 배려를 위한 행동을 더 하는 편이다. ',
                                     '나는 어드레스한 후에도 스윙 기술이나 전략에 대해 과도하게 생각하는 경향이 있다.',
                                     '경기가 잘 풀리지 않거나 실수를 한 후 갑자기 멍해지며 집중이 잘 안 되는 경향이 있다.',
                                     '나는 주의를 기울이지 않고 퍼팅 스트로크하여 짧은 퍼트를 놓치는 편이다.',
                                     '나는 자신감이 떨어지거나 안 될 것 같은 생각이 들거나 소심해져 골프가 안 될 때가 자주 생겨 일관성이 없는 것 같다.',
                                     '나는 어드레스 했을 때 뜬금없이 순간적으로 자신감이 떨어져 그냥 못 칠 것 같은 생각이 들 때가 있다.',
                                     '나는 경기 전이나 경기 중에 나의 능력을 의심하거나 실망하고 좌절하는 경향이 있다.',
                                     '나는 선택한 클럽, 표적, 샷의 유형, 퍼팅 라인, 퍼팅 스피드 등을 완전히 확신하지 못하거나 의심하면서 샷을 실행하는 경우가 있다.',
                                     '나는 나의실력을 충분히 발휘하며 수행할 자신감이 항상 있다.',
                                     '나는 갤러리가 많을 때나 경기를 잘해야 한다는 부담감과 중압감에 긴장하고 불안해하며 경기에 임하는 경우가 있다.',
                                     '나는 어떤 상황의 샷이나 퍼팅을 두려워한다.',
                                     '나는 첫 홀 티샷 전에 긴장을 하는 경향이 있다.',
                                     '나는 위기에 처했을 때 긴장을 하는 경향이 있다.',
                                     '나는 샷이나 퍼팅을 할 때 스윙 템포가 늦어지거나 빨라지는 성향을 가지고 있다는 말을 듣는다.',
                                     '나는 중요한 시합일수록 긴장을 많이 하고 실수를 하는 경향이 있다.',
                                     '나는 경기 중에 타인이 하는 말이나 행동에 불안해지는 경향이 있다.',
                                     '나는 몸이 무겁고 처질 때 활기를 북돋는 것이 어렵다.',
                                     '나는 경기에서 신경질적으로 예민하고, 나 자신과 타인에게 참을성이 없다는 소리를 듣는다.',
                                     '나는 샷을 미스했을 때 실망, 좌절, 화, 짜증을 내며 부정적인 감정 반응을 한다.',
                                     '나는 동반자나 갤러리의 말이나 행동에 짜증을 내거나 불쾌해 하는 경향이 있다.',
                                     '나는 캐디의 잘못과 경기 지연에 화가 나거나  짜증을 내는 경향이 있다.',
                                     '나는 코스 공략을 위한 잘 계획된 최선의 전략 없이 경기를 하는 경우가 있다.',
                                     '나는 중요한 경기에서는 전략을 평소와는 다르게 구사하는 경향이 있다.',
                                     '나는 나의 스코어나 동반자의 스코어에 따라 코스 공략 전략을 수정하는 경향이 있다.',
                                     '나는 홀을 어떻게 공략 할지를 결정 할 때 다른 플레이어들의 선택에 영향을 받는 경향이 있다.',
                                     '나는 샷이나 퍼팅을 결정할 때 바람, 고도차, 그린의 기복 등 반드시 고려해야할 요소를 잊어버리는 경우가 있다.',
                                     '나는 샷이나 퍼팅을 할 때 스윙 기술에 대해 많이 생각하는 경향이 있다.',
                                     '나는 경기 전이나 경기 중에 긍정적, 건설적, 용감한 생각보다 부정적, 단념적인 생각을 하는 경향이 있다.',
                                     '나는 경기 중에 생각을 너무 많아 불안한 경우가 있다. ',
                                     '나는 오비 구역이나 해저드 구역이 눈에 많이 들어와 신경이 쓰이는 경우가 있다.',
                                     '나는 경기 중 남은 홀들과 경기 결과에 대한 기대, 두려움 또는 걱정을 하며 미래의 일을 생각하는 경향이 있다.',
                                     '나는 완벽을 추구하려고 노력하는 경향이 있다.',
                                     '집중이 안 될 때는 노력해도 안 되니까 될 대로 되라는 식으로 편하게 생각 없이 경기를 하는 편이다.',
                                     '나는 나의 경기 모습이나 샷 장면을 생생하게 머릿속으로 그릴 수 있다.',
                                     '나는 경기 전날에 내일의 경기를 훌륭히 수행하는 모습을 화면에서 보는 듯이 생생하게 상상할 수 있다.',
                                     '나는 샷이나 퍼팅을 하기 전에 볼 뒤에 서서 실행할 샷이나 퍼팅의 뚜렷한 이미지를 상상하는 것을 하지 않거나 그렇게 하는 것이 어렵다.',
                                     '나는 샷이나 퍼팅을 하기 전 연습 스윙을 할 때 스윙이나 스트로크의 움직임, 리듬, 템포를 몸으로 느끼지 않거나 그렇게 하는 것이 어렵다.',
                                     '나는 실수한 장면이 떠오를 때, 그 장면을 성공하는 모습으로 바꾸어 상상할 수 있다.'])
    result_labels = ['집중력',
                     '자신감',
                     '불안 및 각성',
                     '감정 조절',
                     '생각 조절',
                     '심상 조절']
    partition = [[i + 1 for i in range(8)],
                 [i + 9 for i in range(5)],
                 [i + 14 for i in range(8)],
                 [i + 22 for i in range(4)],
                 [i + 26 for i in range(12)],
                 [i + 38 for i in range(5)]]
    reverse_scoring = [i + 1 for i in range(12)] + [i + 14 for i in range(24)] + [i + 40 for i in range(2)]
    reverse_constant = 6
    avg_values = {'M': [27.05, 17.57, 27.82, 15.27, 40.98],
                  'F': [25.36, 15.48, 24.83, 14.78, 38.74]}
    stddev_values = {'M': [5.61, 3.87, 5.57, 3.4, 7.51],
                     'F': [5.37, 3.4, 5.67, 3.19, 6.56]}

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateTimeField(default=timezone.now)
    SEX_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='M')
    dumped_scores = models.CharField(max_length=survey_info.num_questions * 10, blank=True)
    comment = models.TextField(default='', blank=True)
    strategy = models.TextField(default='', blank=True)

    def get_results(self):
        loaded_scores = json.loads(getattr(self, 'dumped_scores'))
        for i in Gmet.reverse_scoring:
            loaded_scores[str(i)] = self.reverse_constant - loaded_scores[str(i)]
        partitioned_values = [[] for _ in range(len(self.partition))]
        for i, div in enumerate(self.partition):
            for q_num in div:
                partitioned_values[i].append(loaded_scores[str(q_num)])

        result_values = dict()
        result_values['score_avg'] = []
        result_values['score_sum'] = []
        for i, values in enumerate(partitioned_values):
            result_values['score_avg'].append(np.average(values))
            result_values['score_sum'].append(np.sum(values))

        result_values['t-score'] = []
        for i, (avg, stddev) in enumerate(zip(self.avg_values[getattr(self, 'sex')],
                                              self.stddev_values[getattr(self, 'sex')])):
            result_values['t-score'].append(50.0 + (result_values['score_sum'][i] - avg) / stddev * 10.0)

        for key in ['score_avg', 't-score']:
            result_values[key] = [round(x, 2) for x in result_values[key]]

        return {'date': get_local_date(getattr(self, 'update_time')),
                'scores': result_values['score_avg'],
                't-scores': result_values['t-score']}


class Tops(models.Model):
    full_title = 'IZOF based TOPS Profiling'

    survey_info = SurveyInfo(choices=[1, 2, 3, 4, 5], first_num=1, last_num=36)
    survey_info.set_answer_labels(['전혀 그렇지 않음 (1)',
                                   '그렇지 않음 (2)',
                                   '보통임 (3)',
                                   '약간 그러함 (4)',
                                   '매우 그러함 (5)'])
    survey_info.set_question_labels([
        '경기에서 최선을 다하자는 긍적적인 혼잣말을 한다.',
        '경쟁력 있는 수행에 도움이 되는 말을 마음속으로 한다.',
        '혼잣말을 효과적으로 (관리)한다.',
        '수행에 도움이 되는 구체적인 단서나 말을 말한다.',
        
        '감정이 나의 최상 수행을 방해한다.(R)',
        '중압감 상황에서 감정조절이 안 된다.(R)',
        '화가 나면 실력을 발휘하지 못한다.(R)',
        '실수를 한 후에는 평소처럼 집중하는 것이 어렵다.(R)',

        '기술에 대한 의식적인 생각을 하지 않고 수행한다.',
        '잘 해야겠다는 생각을 하지 않고 저절로 수행되게 한다.',
        '자동적(무의식적)으로 수행한다.',
        '의식적인 노력이 거의 없이 본능적으로 수행(플레이)한다.',

        '개인적인 수행 목표를 설정한다.',
        '매우 구체적인 목표를 설정한다.',
        '구체적인 결과 목표를 설정한다.',
        '경기의 목표를 달성했는지를 평가한다.',

        '경기 전에 경기 루틴(절차)를 상상한다.',
        '수행의 느낌을 상상 속에서 예행연습한다(떠올린다).',
        '수행을 마음속에서 예행연습한다(그린다).',
        '원하는 방향으로 정확하게 경기가 진행되는 것을 시각화한다.',

        '적정 수준으로 활력(에너지)을 높인다.',
        '분발하는데 필요한 것을 실행한다.',
        '수행할 준비가 되도록 나 자신을 분발시킨다.',
        '필요하다고 생각되면 나의 활력(에너지) 수준을 높인다.',

        '실수하는 모습을 상상한다.(R)',
        '부정적인 혼잣말을 한다.(R)',
        '실패를 생각한다.(R)',
        '생각을 긍정적으로 유지한다.',

        '너무 불안할 때 긴장을 풀고 진정할 수 있다.',
        '너무 긴장될 때 긴장을 풀기가 어렵다.(R)',
        '중압감이 생길 때 긴장을 푸는 방법을 알고 있다.',
        '수행할 준비를 해야 할 때 긴장을 풀 수 있다.',

        '컨디션이 좋도록 몸 상태를 준비한다.',
        '컨디션이 좋도록 마음상태를 준비한다.',
        '컨디션 조절하는 나만의 방법이 있다.',
        '시합에 앞서 최고의 컨디션을 찾으려고 노력한다.',
    ])
    result_labels = ['자화',
                     '감정조절',
                     '자동성',
                     '목표설정',
                     '심상',
                     '분발/활성화',
                     '부정적 생각',
                     '이완',
                     '컨디션']
    partition = [[4 * i + j + 1 for j in range(4)] for i in range(9)]
    reverse_scoring = [5, 6, 7, 8, 25, 26, 27, 30]
    reverse_constant = 6

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateTimeField(default=timezone.now)
    dumped_scores = models.CharField(max_length=survey_info.num_questions * 10, blank=True)
    comment = models.TextField(default='', blank=True)
    strategy = models.TextField(default='', blank=True)

    should_comment = models.BooleanField(default=True)

    def get_results(self):
        loaded_scores = json.loads(getattr(self, 'dumped_scores'))
        for i in Tops.reverse_scoring:
            loaded_scores[str(i)] = Tops.reverse_constant - loaded_scores[str(i)]
        partitioned_values = [[] for _ in range(len(Tops.partition))]
        for i, div in enumerate(Tops.partition):
            for q_num in div:
                partitioned_values[i].append(loaded_scores[str(q_num)])
        result_values = dict()
        result_values['levels'] = list(map(np.average, partitioned_values))
        result_values['levels'] = list(map(lambda x: str(round(x, 2)), result_values['levels']))
        result_values['average_level'] = str(round(np.average(list(loaded_scores.values())), 2))
        return {'date': get_local_date(getattr(self, 'update_time')),
                'levels': result_values['levels'],
                'average_level': result_values['average_level']}


class Fss(models.Model):
    full_title = 'IZOF based FSS Profiling'

    survey_info = SurveyInfo(choices=[1, 2, 3, 4, 5], first_num=1, last_num=36)
    survey_info.set_answer_labels(['전혀 그렇지 않음 (1)',
                                   '그렇지 않음 (2)',
                                   '보통임 (3)',
                                   '약간 그러함 (4)',
                                   '매우 그러함 (5)'])
    survey_info.set_question_labels(['나는 도전/위기에 직면했다. 그러나 나는 그 도전/위기를 받아들일(맞설) 충분한 기술을 가지고 있다고 믿었다.',
                                     '나는 정확하게 움직이려고 생각하지 않고도 정확하게 움직였다.',
                                     '내가 하고자 하는 것을 분명히 알았다.',
                                     '내가 잘하고 있었다는 것이 정말 분명했다.',
                                     '내 주의는 내가 하고 있는 것에 전적으로 맞추어져(집중되어) 있었다.',
                                     '내가 하고 있었던 것에 대한 완전한 통제/제어를 느꼈다.',
                                     '나는 다른 사람이 나에 대해 생각하고 있었을지도 모를 것에 신경 쓰지 않았다.',
                                     '시간이 변형되는 것 같다. (늦어지거나 빨라지거나)',
                                     '나는 정말로 경험을 즐겼다.',
                                     '내 능력은 엄청난 도전/위기 상황에 부합(적합)했다.',
                                     '모든 것들이 그저 자동적으로 일어나는 것 같았다.',
                                     '나는 하고 싶은 것에 대한 강한 감각을 가졌다.',
                                     '내가 얼마나 잘 수행하고 있었는지를 알았다.',
                                     '일어나고 있었던 것에 마음을 유지하려고 노력하지 않았다.',
                                     '나는 내가 하고 있던 것을 제어/통제할 수 있다고 느꼈다.',
                                     '나는 경기에서의 수행을 걱정하지 않았다.',
                                     '시간이 보통 때와 다르게 흘러가는 듯했다.',
                                     '나는 그 수행의 느낌을 사랑했고 그 느낌을 다시 느끼고 싶다.',
                                     '나는 그 상황의 높은 요구(부담감)를 감당할 만큼 충분히 유능하다고 느꼈다.',
                                     '나는 자동적으로 수행했다.',
                                     '내는 무엇을 성취하고 싶은지를 알고 있었다.',
                                     '나는 수행하고 있는 동안 내가 얼마나 잘하고 있는지에 대한 좋은 느낌(신념)을 가졌다.',
                                     '나는 완전한 집중력을 가졌다.',
                                     '나는 완전한 제어 느낌(통제감)을 가졌다.',
                                     '나는 나 자신을 어떻게 나타내는지에 관심이 없었다.',
                                     '수행을 하는 동안 시간이 멈춘 것처럼 느껴졌다.',
                                     '나는 그 경험에서 희열을 느꼈다.',
                                     '도전(위기)과 나의 기술은 똑같이 높은 수준이었다.',
                                     '나는 생각할 필요 없이 자연스럽고 자동적으로 플레이했다.',
                                     '나의 목표가 분명히 정해졌다.',
                                     '나는 내가 얼마나 잘하고 있었는지를 수행 도중에 말할 수 있었다.',
                                     '나는 당면 과제에 완전히 집중되었다.',
                                     '나는 신체에 대한 완전한 제어감(통제감)을 느꼈다.',
                                     '나는 다른 사람이 나에 대해 무엇을 생각하고 있었는지에 대해 걱정하지 않았다.',
                                     '가끔은 일들이 거의 느리게 일어나고 있었던 것 같았다.',
                                     '나는 그 경험이 아주 보람되다는 것을 알았다.'])
    result_labels = ['Challenge-skill balance(도전과 기술의 균형)',
                     'Action-awareness merging(활동과 인식의 통합)',
                     'Clear goals(명확한 목표)',
                     'Unambiguous feedback(분명한 피드백)',
                     'Concentration on task at hand(당면 과제에의 집중)',
                     'Paradox of control(통제감)',
                     'Loss of self-consciousness(자의식 상실)',
                     'Transformation of time(시간의 변형)',
                     'Autotelic experience(자기 목적적 경험)']
    partition = [[1, 10, 19, 28],
                 [2, 11, 20, 29],
                 [3, 12, 21, 30],
                 [4, 13, 22, 31],
                 [5, 14, 23, 32],
                 [6, 15, 24, 33],
                 [7, 16, 25, 34],
                 [8, 17, 26, 35],
                 [9, 18, 27, 36]]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateTimeField(default=timezone.now)
    dumped_scores = models.CharField(max_length=survey_info.num_questions * 10, blank=True)
    comment = models.TextField(default='', blank=True)
    strategy = models.TextField(default='', blank=True)

    def get_results(self):
        loaded_scores = json.loads(getattr(self, 'dumped_scores'))
        partitioned_scores = [[] for _ in range(len(Fss.partition))]
        for i, div in enumerate(Fss.partition):
            for q_num in div:
                partitioned_scores[i].append(loaded_scores[str(q_num)])
        result_values = dict()
        result_values['levels'] = list(map(np.average, partitioned_scores))
        result_values['levels'] = list(map(lambda x: str(round(x, 2)), result_values['levels']))
        result_values['average_level'] = str(round(np.average(list(loaded_scores.values())), 2))
        return {'date': get_local_date(getattr(self, 'update_time')),
                'levels': result_values['levels'],
                'average_level': result_values['average_level']}


class Acsi(models.Model):
    full_title = 'IZOF based ACSI-28 Profiling'

    survey_info = SurveyInfo(choices=[1, 2, 3, 4, 5], first_num=1, last_num=28)
    survey_info.set_answer_labels(['전혀 그렇지 않음 (1)',
                                   '그렇지 않음 (2)',
                                   '보통임 (3)',
                                   '약간 그러함 (4)',
                                   '매우 그러함 (5)'])
    survey_info.set_question_labels(['나는 해야할 구체적인 목표를 매일 또는 주 단위로 설정한다.',
                                     '나는 나의 재능과 기술을 최대한 발휘한다.',
                                     '코치나 메니저가 실수를 어떻게 수정해야 하는지 알려줄 때, 나는 사적 감정으로 심각하게 받아들이거나 속이 상하는/화나는 경향이 있다.',
                                     '나는 경기 할 때, 주의를 집중하고 집중을 방해하는 주의산만 요소를 차단할 수 있다.',
                                     '나는 경기가 잘 풀리지 않는 것과 상관없이, 경기를 하는 동안 긍정심과 열정을 유지한다.',
                                     '나는 중압감 상황에서 더욱 명확하게 생각하기 때문에 수행을 더 잘하는 경향이 있다.',
                                     '나는 다른 사람이 나의 수행을 생각하는 것에 대해 상당히 많이 걱정한다.',
                                     '나는 목표에 도달하는 방법에 대해 많은 계획을 세운다.',
                                     '나는 경기를 잘할 것이라는 자신감을 느낀다.',
                                     '코치나 매니저가 나를 바판할 때, 나는 도움을 받는다기 보다는 속이 상하게 된다.',
                                     '주의산만한 생각이 내가 보거나 듣고 있는 것을 방해하지 못하게 하는 것이 쉽다.',
                                     '내가 어떻게 수행할 것인지에 대한 걱정으로 인해 많은 중압감을 받는다/느낀다.',
                                     '나는 모든 연습에서 자신만의 수행 목표를 설정한다.',
                                     '나는 열심히 연습하거나 경기하도록 강요/독려받을 필요가 없다; 나는 최선을 다한다.',
                                     '코치가 나에게 비판하거나 소리지르면, 나는 속상해/화내지 하지 않고 그 실수를 수정한다.',
                                     '나는 경기에서 예상치 못한 상황을 매우 잘 다룬다/처리한다.',
                                     '경기가 잘 안될 떄, 나는 침착함/차분함을 유지하라고 나에게 말하고, 이것이 나에게 효과가 있다.',
                                     '나는 경기를 하는 동안 중압감이 커질수록, 중압감을 더욱 더 즐긴다.',
                                     '경쟁/경기를 하는 동안, 나는 실수하거나 실패하지 않을까 하고 걱정한다.',
                                     '나는 경기가 시작되기 오래 전에 생각해낸 나 자신만의 경기 계획을 가지고 있다.',
                                     '나는 너무 긴장된다고 느낄 때, 곧바로 내 몸을 이완시키고 스스로를 진정시킬 수 있다.',
                                     '나에게 중압감 상황은 반가운 도전이다.',
                                     '내가 실패하거나 경기를 망치거나 정신적으로 맛이 갈 때 어떤 일이 벌어질지를 생각하고 상상한다.',
                                     '나에게 어떤일이 벌어져도 감정 조절을 유지한다.',
                                     '나는 하나의 물체나 사람에게 주의를 기울이고 집중하는 것이 쉽다.',
                                     '목표 성취에 실패했을 때, 그 실패로 인해 나는 더욱 열심히 노력한다.',
                                     '나는 기술을 향상시키기 위해 코치나 매니저의 충고와 가르침을 주의깊게 듣는다.',
                                     '나는 중압감이 올 때 더 잘 집중하기 때문에 실수가 줄어든다/많지 않다.'])
    result_labels = ['Coping With Adversity(역경 대처)',
                     'Peaking Under Pressure(중압감에서의 최상 수행)',
                     'Goal Setting and Mental Preparation(목표설정 및 정신적 준비)',
                     'Concentration(집중력)',
                     'Freedom From Worry(걱정으로부터의 해방)',
                     'Confidence and Achievement Motivation(자신감 및 성취동기)',
                     'Coachability(지도가능 상태)']
    partition = [[5, 17, 21, 24],
                 [6, 18, 22, 28],
                 [1, 8, 13, 20],
                 [4, 11, 16, 25],
                 [7, 12, 19, 23],
                 [2, 9, 14, 26],
                 [3, 10, 15, 27]]
    reverse_scoring = [3, 7, 10, 12, 19, 23]
    reverse_constant = 6

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateTimeField(default=timezone.now)
    dumped_scores = models.CharField(max_length=survey_info.num_questions * 10, blank=True)
    comment = models.TextField(default='', blank=True)
    strategy = models.TextField(default='', blank=True)

    def get_results(self):
        loaded_scores = json.loads(getattr(self, 'dumped_scores'))
        for i in Acsi.reverse_scoring:
            loaded_scores[str(i)] = Acsi.reverse_constant - loaded_scores[str(i)]
        partitioned_scores = [[] for _ in range(len(Acsi.partition))]
        for i, div in enumerate(Acsi.partition):
            for q_num in div:
                partitioned_scores[i].append(loaded_scores[str(q_num)])
        result_values = dict()
        result_values['levels'] = list(map(np.average, partitioned_scores))
        result_values['levels'] = list(map(lambda x: str(round(x, 2)), result_values['levels']))
        result_values['average_level'] = str(round(np.average(list(loaded_scores.values())), 2))
        return {'date': get_local_date(getattr(self, 'update_time')),
                'levels': result_values['levels'],
                'average_level': result_values['average_level']}


class CourseManagement(models.Model):
    full_title = 'IZOF based Course Management Profiling'

    survey_info = SurveyInfo(choices=[1, 2, 3, 4, 5], first_num=1, last_num=39)
    survey_info.set_answer_labels(['전혀(Never)',
                                   '드물게(Poor)',
                                   '가끔/조금/적당히(Fair)',
                                   '자주/많이/충분히(Good)',
                                   '항상/모두/확실히(Excellent)'])
    survey_info.set_question_labels(['1. 각 클럽별 거리를 알고있다.',
                                     '2. 거리 목과 스코어 카드를 이용해 타겟까지의 거리 계산을 한다.',
                                     '3.그린의 빠르기와 딱딱한 정도를 확인한다.',
                                     '4. 사용하는 클럽을 신뢰한다(나에게 맞다고 믿는다).',
                                     '5. 여러가지 잔디들의 다양한 특성들을 알고있다.',
                                     '6. 경기 조건에 대한 대처 계획을 수립하고 플레이 한다. (경기 조건 : 바람, 습도, 온도변화, 비, 고도, 잔디 결, 바다, 호수, 산 등)',
                                     '7. 홀의 위치를 예측하고 계산 하는 능력이 있다.',
                                     '1. 자신에게 가장 잘 맞고 마음에 들며 공격적으로 플레이 할 홀들을 선택한다.',
                                     '2. 자기와 잘 맞지 않고 신중하고 조심스럽게 플레이 할 홀들을 결정한다',
                                     '3. 모든 샷에 대해 어느 지점을 겨냥 할지를 계획하고 시각화(상상)한다.(티 샷)',
                                     '4. 낯선 코스에서의 경기를 위한 준비: 트러블 지역들을 확인하고, 거리 목들의 위치를 찾아내고 그린까지의 거리에 대한 감각을 익힌다',
                                     '1. Warm-up(준비 운동)으로 근육을 이완시킨다',
                                     '2. 연습을 하며 그날의 경기에 영향을 미칠 볼 비행 경향들을 확인한다.',
                                     '3. 연습에서 그날이나 그 코스에 유용한 스윙을 결정 및 선택한다',
                                     '4. 연습에서 그날의 목표를 선택한다.(Good -> Better -> Better -> Best)',
                                     '5. 연습에서 그날이나 그 코스에 유용한 클럽을 선택한다.',
                                     '6. 연습에서 일관된 Pre-Shot Routine 실행을 점검한다.',
                                     '1. 아주 특별하지 않은 상황에서는 라운드를 B-Game으로 시작한다.',
                                     '2. 게임 도중에 꼭 필요한 경우 A-Game이나 C-Game으로 전략 수준을 수정한다.',
                                     '1. 플레이 할 샷의 위험/보상 상황에 대한 정직한 평가를 하여 판단과 결정을 한다.',
                                     '2. 코스에서 외부 자극이 아닌 그날 자신의 기술 수준에만 근거하여 목표, 클럽, 샷의 종류를 선택한다.',
                                     '3. 50% 이상의 성공 가능성이 있다고 판단되면 그 기술을 이용하는 전략을 선택한다.',
                                     '4. 그린 주변에서의 판단과 결정은 Putting > chipping > Pitching > Bump & run > Lob Shot 등의 순서로 한다.',
                                     '1. 편안하게 깃대로 샷을 하기에 충분한 클럽을 사용한다.',
                                     '2. 모든 샷에 일관된 루틴을 하며 경기한다. (시각화 포함)',
                                     '3. 성공 가능한 퍼팅을 짧게 하지 않는다.',
                                     '4. 맞바람과,  포대 그린을 향한 오르막에서, 긴 클럽을 사용한다; 반대 상황에서, 짧은 클럽을 사용한다.',
                                     '5. 샷 실행 전에 부정적인 생각이 들면 샷을 하지 않고 프리샷 루틴을 새로 시작한다.',
                                     '6. 평소보다 더 많은 노력으로 스윙 하지 않는다.',
                                     '1. 자신이 할 수 없는 것은 절대 시도하지 않는다.',
                                     '2. 자신의 강점과 약점들을 잘 알고있다.',
                                     '3. 자신의 경기 방식과 경향을 잘 알고있다.',
                                     '1. 스트레이트 샷으로 인해 손해를 볼 지점을 겨냥하지 않는다.',
                                     '2. 티에서는 다른 샷보더 다소 보수적으로 플레이한다.',
                                     '3. 홀에 가까울수록 더 공격적(적극적)으로 플레이 한다',
                                     '4. 어프로우치 샷에서는 다음 샷을 가능한 한 쉽게 만드는 전략으로 플레이한다. (클럽 선택)',
                                     '5. 표적 샷은 솔직하고 공정하게 스스로를 평가하여 성공 자신이 있는 신뢰구역으로 한다.',
                                     '6. 그린 위에서는 홀에 가까울수록 더 공격적이고 대담하게 플레이하고, 홀에서 멀리 있을수록 더 신중하고 조심스럽게 플레이 한다.',
                                     '7. 트러블 샷은 성공이 상당히 확실할 때를 제외하고는 모험을 하지 않고 볼을 플레이 할 수 있는 곳에 되돌려 놓는다.'])
    # result_labels = ['Basic',
    #                  'Game plan',
    #                  'Decision-making process',
    #                  'Stroke-saver system',
    #                  'Game Control Strategies']
    result_labels = ['Basic(기초정보이용)',
                     'Game plan(경기계획)',
                     'Decision-making process(의사결정과정)',
                     'Stroke-saver system(다수관리시스템)',
                     'Game Control Strategies(경기조절전략)']
    partition = [[i + 1 for i in range(7)],
                 [i + 8 for i in range(12)],
                 [i + 20 for i in range(4)],
                 [i + 24 for i in range(6)],
                 [i + 30 for i in range(10)]]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateTimeField(default=timezone.now)
    dumped_scores = models.CharField(max_length=survey_info.num_questions * 10, blank=True)
    comment = models.TextField(default='', blank=True)
    strategy = models.TextField(default='', blank=True)

    def get_results(self):
        loaded_scores = json.loads(getattr(self, 'dumped_scores'))
        partitioned_scores = [[] for _ in range(len(CourseManagement.partition))]
        for i, div in enumerate(CourseManagement.partition):
            for q_num in div:
                partitioned_scores[i].append(loaded_scores[str(q_num)])
        result_values = dict()
        result_values['levels'] = list(map(np.average, partitioned_scores))
        result_values['levels'] = list(map(lambda x: str(round(x, 2)), result_values['levels']))
        result_values['average_level'] = str(round(np.average(list(loaded_scores.values())), 2))
        return {'date': get_local_date(getattr(self, 'update_time')),
                'levels': result_values['levels'],
                'average_level': result_values['average_level']}
