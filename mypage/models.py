#-*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json


TABLE_WIDTH = {
    0: 'narrow',
    1: 'wide',
}
STRATEGY_TYPE = {
    0: '행동전략',
    1: '인지전략',
    2: '이완반응',
}


class PreshotRoutine(models.Model):
    strategy_labels = [
        '정보 수집 및 판단',
        '수행 계획 결정',
        '정신적 - 신체적 예행연습(Rehearsal Swing)',
        '볼 비행 시각화',
        '어드레스',
        '표적 응시 및 집중',
        '실행',
    ]
    # format: [(TABLE_WIDTH, STRATEGY_TYPE, CONTENT), ...]
    strategies = [
        [
            (0, 0, '볼로 다가가며 프리샷 루틴을 시작한다.'),
            (0, 0, '필요하면 주변으로 움직이며 정보를 수집한다.'),
            (0, 0, '필요하면 캐디와 상의한다.'),
            (0, 0, '퍼팅 - 볼과 홀 주위를 돌며 그린을 읽는다.'),
            (0, 1, '상황에 대한 다양한 정보를 종합적으로 수집 및 계산하여 과제 상황을 판단한다.'),
            (1, 0, '상황정보 - 표적의 위치(거리)/표적 주변 및 그린의 상황(경사도, 기복, 그린 스피드, 그린 경도)/벙커, 해저드/볼이 놓여있는 곳의 경사도, 잔디 결, 잔디 깊이/볼과 홀 위치의 고도차/바람/습도/비/온도/호수, 바다, 산의 위치 등'),
        ],
        [
            (0, 0, '클럽을 선택한다. 티샷은 티업 한다.'),
            (0, 0, '필요하면 케디와 상의한다.'),
            (0, 0, '퍼팅 - 퍼팅 라인에 맞추어 볼을 놓고 마크를 집고 퍼팅 라인이 맞는지 확인한다.'),
            (0, 1, '목표를 설정하고 전략, 즉 공략지점, 클럽, 수행할 샷의 유형에 대한 수행 계획을 결정을 한다. 결정에 완전히 전념한다.'),
            (0, 1, '퍼팅 – 볼 뒤에서 퍼팅 라인을 시각화한다.'),

        ],
        [
            (0, 0, '볼의 뒤나 옆에서 한두 번의 부드러운 연습 스윙(풀스윙이나 부분 스윙)을 실행한다.'),
            (0, 0, '퍼팅 - 볼 뒤나 옆에 어드레스 하여 퍼팅라인을 보거나 지면을 보면서 연습 스트로크를 두세 번 한다.'),
            (0, 1, '리듬이나 템포와 같은 일반적인 수행 단서나 한두 가지 구체적인 기술 단서를 가지고 신체 움직임을 정신적으로 연습하며 최상의 샷 실행을 위한 이상적인 운동감각적 움직임을 몸과 마음으로 느낀다.  필요하면 자기중심적인 마음가짐으로 자신감이나 과정중심적인 생각을 촉진시키는 자화나 행동을 한다.'),
            (1, 2, '필요하면 깊은 숨을 쉬며 몸과 마음을 이완한다.(샷과 퍼팅 모두) 또는 워밍업을 하며 몸과 마음을 활성화시킨다.(퍼팅은 제외)'),
        ],
        [
            (0, 0, '볼 뒤에 서서 볼비행선 또는 퍼팅 라인을 확인한다.'),
            (0, 1, '볼이 표적으로 정확하게 날아가 착지하는 장면을 마음속에 그리며 볼 비행을 시각화한다. 필요하면 자기중심적이고 미래지향적인 마음가짐으로 긍정적인 결과에 대한 생각이나 자화를 한다.'),
            (0, 1, '퍼팅 - 볼 뒤에서 연습 스트로크를 하는 경우 볼이 굴러서 홀로 들어가는 장면을 시각화한다.'),
            (1, 2, '필요하면 깊은 숨을 쉬며 몸과 마음을 이완한다.'),
        ],
        [
            (0, 0, '구체적이고 명확하고 일관된 행동으로 볼에 어드레스하며 그립(grip), 클럽해드 조준/신체 정렬(aim/alignment), 셋업(setup)을 한다.'),
        ],
        [
            (0, 0, '표적(선)을 한두 번 응시한다.'),
            (0, 1, '표적과 볼에 주의를 집중한다.  필요하면 자기중심적이고 미래지향적이고 과정중심적인 마음가짐으로 수행에의 주의집중을 촉진시키는 생각이나 자화를 한다.'),
            (1, 2, '이완을 위한 자신만의 구체적인 행동 전략을 실행한다. 이완전략 - 클럽 웨글, 부분 스윙, 그립 악력 조절, 심호흡, 포워드 프레스(forward press) 등'),
        ],
        [
            (0, 0, '자신의 스윙 단서를 이용하거나 운동감각적 느낌으로 자동적이고 본능적으로 지체 없이 실행한다.'),
            (0, 0, '퍼팅 - 실행 직후 잠시 동안 볼 지점을 계속 본다. 그 후 퍼팅 결과를 확인한다.'),
            (1, 0, '부정적인 생각이나 의심(Second-Guessing)이 들면, 실행을 멈추고 프리샷 루틴 첫 단계부터 전 과정을 다시 시작한다.'),
        ]
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateTimeField(default=timezone.now)
    dumped_strategies = models.TextField(blank=True)


class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateTimeField(default=timezone.now)
    date = models.DateField(blank=False)
    competition_level = models.IntegerField( blank=True)
    competition_name = models.TextField( blank=True)
    dumped_contents = models.TextField(blank=True)


class LongTermGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateField(default=timezone.now)
    dumped_contents = models.TextField(blank=True)
    def getDumpedContents(self) :
        return json.loads(self.dumped_contents)


class DailyGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateField(default=timezone.now)
    dumped_contents = models.TextField(blank=True)