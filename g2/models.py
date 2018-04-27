#-*- coding: utf-8 -*-

import json
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class GolfSwing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateTimeField(default=timezone.now)
    dumped_contents = models.TextField(blank=True)
    video = models.TextField(blank=True)

    @classmethod
    def get_categories(cls):
        first_categories = cls._get_first_categories()
        second_categories = cls._get_second_categories()
        third_categories = cls._get_third_categories()

        assert len(first_categories) == len(second_categories)

        second_category_count = 0
        for sub_second_categories in second_categories:
            for _ in sub_second_categories:
                second_category_count += 1
        assert second_category_count == len(third_categories)

        result = []
        second_category_index = 0
        for i, first_category in enumerate(first_categories):
            result.append([first_category, []])
            for j, second_category in enumerate(second_categories[i]):
                result[i][1].append([second_category, []])
                for third_category in third_categories[second_category_index]:
                    result[i][1][j][1].append([third_category, "", ""])
                second_category_index += 1
        return result

    def fill_contents(self):
        result = self.get_categories()

        if self.dumped_contents:
            contents_dict = json.loads(self.dumped_contents)
            for key, value in contents_dict.items():
                key_tokens = key.split("_")
                first_category_index = int(key_tokens[1])
                second_category_index = int(key_tokens[2])
                third_category_index = int(key_tokens[3])

                if key_tokens[0] == "comment":
                    result[first_category_index][1][second_category_index][1][third_category_index][1] = value
                elif key_tokens[0] == "drill":
                    result[first_category_index][1][second_category_index][1][third_category_index][2] = value
        return result
    @staticmethod
    def _get_first_categories():
        return [
            "Pre-Swing Fundamental",
            "In-Swing Fundamental",
            "Ball Flight",
        ]
    @staticmethod
    def _get_second_categories():
        return [
            [
                "Grip(Dir)\n그립",
                "Aim(Dir)\n조준",
                "Alignment(Dir)\n신체정렬",
                "Setup(DD)\n셋업",
            ],
            [
                "Dynamic Balance(DD)\n체중이동",
                "Swing Center(DD)\n스윙 중심",
                "Swing Plane(Dir)\n스윙 플레인",
                "Body Rotation\n신체 회전",
                "Length of Arc(Dist)\n스윙아크 길이백스윙 탑 위치",
                "Width of Arc(Dist)\n스윙아크 넓이",
                "Lever System(Dist)\n지레작용",
                "Position(Dir)\n백스윙 탑 위치",
                "Transition\n전환",
                "Release(Dir)\n릴리즈",
                "Impact(DD)\n임팩트",
                "Connection(DD)\n연결/신체협응",
                "Timing(DD)\n타이밍",
                "Rhythm & Tempo\n리듬 & 템포",
            ],
            [
                "Ball Flight\n볼 비행 경향",
            ],
        ]

    @staticmethod
    def _get_third_categories():
        return [
            [
                "4P",
                "V Parallel",
                "Thumb",
            ],
            [
                "Open/Closed",
            ],
            [
                "Right/Left",
            ],
            [
                "Posture",
                "Weight Distribution",
                "Ball Position",
            ],
            [
                "Backswing",
                "Downswing",
                "F - Through",
            ],
            [
                "Backswing",
                "Downswing",
                "F - Through",
            ],
            [
                "Backswing",
                "Top position",
                "Downswing",
                "F - Through",
            ],
            [
                "Upper",
                "Lower",
            ],
            [
                "Backswing",
                "F - Through",
            ],
            [
                "Backswing",
                "Extension",
            ],
            [
                "Backswing",
            ],
            [
                "",
            ],
            [
                "",
            ],
            [
                "Timing",
                "F - arm Rotation",
                "Uncocking",
            ],
            [
                "Centered",
                "Face Angle",
            ],
            [
                ""
            ],
            [
                "Ground - Up",
            ],
            [
                "",
            ],
            [
                "Distance",
                "Direction",
                "Trajectory",
            ],
        ]


class ShortGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateTimeField(default=timezone.now)
    dumped_contents = models.TextField(blank=True)
    video = models.TextField(blank=True)
    @classmethod
    def get_categories(cls):
        first_categories = cls._get_first_categories()
        second_categories = cls._get_second_categories()
        third_categories = cls._get_third_categories()

        assert len(first_categories) == len(second_categories)

        second_category_count = 0
        for sub_second_categories in second_categories:
            for _ in sub_second_categories:
                second_category_count += 1
        assert second_category_count == len(third_categories)

        result = []
        second_category_index = 0
        for i, first_category in enumerate(first_categories):
            result.append([first_category, []])
            for j, second_category in enumerate(second_categories[i]):
                result[i][1].append([second_category, []])
                for third_category in third_categories[second_category_index]:
                    result[i][1][j][1].append([third_category, "", ""])
                second_category_index += 1

        return result

    def fill_contents(self):
        result = self.get_categories()

        if self.dumped_contents:
            contents_dict = json.loads(self.dumped_contents)

            for key, value in contents_dict.items():
                key_tokens = key.split("_")
                first_category_index = int(key_tokens[1])
                second_category_index = int(key_tokens[2])
                third_category_index = int(key_tokens[3])

                if key_tokens[0] == "comment":
                    result[first_category_index][1][second_category_index][1][third_category_index][1] = value
                elif key_tokens[0] == "drill":
                    result[first_category_index][1][second_category_index][1][third_category_index][2] = value

        return result

    @staticmethod
    def _get_first_categories():
        return [
            "Pre-Swing Fundamentals",
            "In-Swing Fundamentals",
            "Ball Flight",
        ]

    @staticmethod
    def _get_second_categories():
        return [
            [
                "Grip\n그립",
                "Aim\n조준",
                "Alignment\n신체정렬",
                "Posture\n자세",
                "Ball Position\n볼 위치",
            ],
            [
                "Dead Hands\n손목 사용 정도",
                "Synch.Body Turn\n신체회전 동기화",
                "Swing Center\n스윙 중심",
                "Swing Plane\n스윙 플레인",
                "Left Arm\n왼팔 펴짐",
                "Short - to - Long\n짧고-길게: 가속",
                "Finish\n피니쉬",
                "Rhythm\n리듬",
                "Tempo\n템포",
            ],
            [
                "Distance\n거리조절",
                "Direction\n방향조절",
            ],
        ]

    @staticmethod
    def _get_third_categories():
        return [
            [
                "Neutral",
                "Grip Down",
            ],
            [
                "Open / Closed",
            ],
            [
                "Right / Left",
            ],
            [
                "Upright",
                "Weight Distribution",
            ],
            [
                "Chip",
                "Pitch",
                "Send / Lob",
            ],
            [
                "Chip",
                "Pitch",
            ],
            [
                "",
            ],
            [
                "Left",
            ],
            [
                "Upright",
            ],
            [
                "Straight",
            ],
            [
                "Acceleration",
            ],
            [
                "Longer",
            ],
            [
                "",
            ],
            [
                "",
            ],
            [
                "Control",
            ],
            [
                "Control",
            ],
        ]


class Putting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update_time = models.DateTimeField(default=timezone.now)
    dumped_contents = models.TextField(blank=True)
    video = models.TextField(blank=True)
    @classmethod
    def get_categories(cls):
        first_categories = cls._get_first_categories()
        second_categories = cls._get_second_categories()
        third_categories = cls._get_third_categories()

        assert len(first_categories) == len(second_categories)

        second_category_count = 0
        for sub_second_categories in second_categories:
            for _ in sub_second_categories:
                second_category_count += 1
        assert second_category_count == len(third_categories)

        result = []
        second_category_index = 0
        for i, first_category in enumerate(first_categories):
            result.append([first_category, []])
            for j, second_category in enumerate(second_categories[i]):
                result[i][1].append([second_category, []])
                for third_category in third_categories[second_category_index]:
                    result[i][1][j][1].append([third_category, "", ""])
                second_category_index += 1

        return result

    def fill_contents(self):
        result = self.get_categories()

        if self.dumped_contents:
            contents_dict = json.loads(self.dumped_contents)

            for key, value in contents_dict.items():
                key_tokens = key.split("_")
                first_category_index = int(key_tokens[1])
                second_category_index = int(key_tokens[2])
                third_category_index = int(key_tokens[3])

                if key_tokens[0] == "comment":
                    result[first_category_index][1][second_category_index][1][third_category_index][1] = value
                elif key_tokens[0] == "drill":
                    result[first_category_index][1][second_category_index][1][third_category_index][2] = value

        return result

    @staticmethod
    def _get_first_categories():
        return [
            "Pre-Swing Fundamentals",
            "In-Swing Fundamentals",
            "Others",
        ]

    @staticmethod
    def _get_second_categories():
        return [
            [
                "Aim\n조준",
                "Alignment\n신체정렬",
                "Ball Position\n볼 위치",
                "Posture\n자세",
                "Hand Position\n손 위치",
                "Shaft & Forearm\n샤프트와 팔뚝 각도",
            ],
            [
                "Face Angle\n퍼터페이스 각도",
                "Head Path\n퍼터헤드 경로",
                "Sweetspot\n스윗스팟 정타",
                "Dead Hands\n손목 사용 정도",
                "Pulling Motion\n끌어당기는 동작",
                "Acceleration\n가속",
                "No Spin\n볼 회전(스핀)",
                "Rhythm\n리듬",
                "Tempo\n템포",
            ],
            [
                "Distance Control\n거리조절",
                "Green Reading\n그린 읽기",
            ],
        ]

    @staticmethod
    def _get_third_categories():
        return [
            [
                "Open / Closed",
            ],
            [
                "Right / Left",
            ],
            [
                "R - to - L",
                "F - to - B",
            ],
            [
                "Stance Width",
                "Weight Distribution",
                "Elbow Bend",
            ],
            [
                "R - to - L",
                "Below Shoulder",
            ],
            [
                "Straight",
            ],
            [
                "83 %",
            ],
            [
                "17 %",
            ],
            [
                "",
            ],
            [
                "Cupping",
                "Forearm Rotation",
            ],
            [
                "",
            ],
            [
                "20 % <",
            ],
            [
                "",
            ],
            [
                "",
            ],
            [
                "",
            ],
            [
                "",
            ],
            [
                "",
            ],
        ]

