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
                "Grip(Dir)",
                "Aim(Dir)",
                "Alignment(Dir)",
                "Setup(DD)",
            ],
            [
                "Dynamic Balance(DD)",
                "Swing Center(DD)",
                "Swing Plane(Dir)",
                "Body Rotation",
                "Length of Arc(Dist)",
                "Width of Arc(Dist)",
                "Lever System(Dist)",
                "Position(Dir)",
                "Transition",
                "Release(Dir)",
                "Impact(DD)",
                "Connection(DD)",
                "Timing(DD)",
                "Rhythm & Tempo",
            ],
            [
                "Ball Flight",
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
                "Grip",
                "Aim",
                "Alignment",
                "Posture",
                "Ball Position",
            ],
            [
                "Dead Hands",
                "Synch.Body Turn",
                "Swing Center",
                "Swing Plane",
                "Left Arm",
                "Short - to - Long",
                "Finish",
                "Rhythm",
                "Tempo",
            ],
            [
                "Distance",
                "Direction",
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
                "Aim",
                "Alignment",
                "Ball Position",
                "Posture",
                "Hand Position",
                "Shaft & Forearm",
            ],
            [
                "Face Angle",
                "Head Path",
                "Sweetspot",
                "Dead Hands",
                "Pulling Motion",
                "Acceleration",
                "No Spin",
                "Rhythm",
                "Tempo",
            ],
            [
                "Distance Control",
                "Green Reading",
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

