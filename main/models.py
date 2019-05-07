# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.core.urlresolvers import reverse


class Member(models.Model):
    # User class from django.contrib.auth
    # utilizing [username(id), password1, password2] fields
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    # 이름
    full_name = models.CharField(
        max_length=50,
        blank=False
    )
    # 성별
    sex = models.CharField(
        max_length=10,
        choices=(
            ('M', u'남자'),
            ('F', u'여자'),
        ),
        blank=False
    )
    # 소속
    association = models.CharField(
        max_length=100,
        blank=False
    )
    # 핸디캡 (회원가입시 입력받지 않음)
    handicap = models.FloatField(
        blank=True,
        null=True
    )
    # 이메일
    email = models.EmailField(
        blank=True,
        null=True
    )
    # 전화번호
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    # 생년월일
    birth = models.DateField(
        blank=True,
        null=True
    )
    def delete(self):
        print(self.user.username)
        user=User.objects.get(username=self.user.username)
        user.delete()
        print('del')
    # 권한
    permission_g1 = models.BooleanField(default=False)
    permission_g2 = models.BooleanField(default=False)
    permission_g3 = models.BooleanField(default=False)
    permission_g4 = models.BooleanField(default=False)
    permission_mypage = models.BooleanField(default=False)


class MemberAdmin(admin.ModelAdmin):
    def delete_selected(self,request,obj):
        for o in obj.all():
            user=User.objects.get(username=o.user.username)
            user.delete()

    def allow_g1(self, request, queryset):
        rows_updated = queryset.update(permission_g1=True)
        self.message_user(request, "{}명 G1 사용 권한 부여 완료".format(rows_updated))
    allow_g1.short_description = "권한 부여: G1"

    def disallow_g1(self, request, queryset):
        rows_updated = queryset.update(permission_g1=False)
        self.message_user(request, "{}명 G1 사용 권한 박탈 완료".format(rows_updated))
    disallow_g1.short_description = "권한 박탈: G1"

    def allow_g2(self, request, queryset):
        rows_updated = queryset.update(permission_g2=True)
        self.message_user(request, "{}명 G2 사용 권한 부여 완료".format(rows_updated))
    allow_g2.short_description = "권한 부여: G2"

    def disallow_g2(self, request, queryset):
        rows_updated = queryset.update(permission_g2=False)
        self.message_user(request, "{}명 G2 사용 권한 박탈 완료".format(rows_updated))
    disallow_g2.short_description = "권한 박탈: G2"

    def allow_g3(self, request, queryset):
        rows_updated = queryset.update(permission_g3=True)
        self.message_user(request, "{}명 G3 사용 권한 부여 완료".format(rows_updated))
    allow_g3.short_description = "권한 부여: G3"

    def disallow_g3(self, request, queryset):
        rows_updated = queryset.update(permission_g3=False)
        self.message_user(request, "{}명 G3 사용 권한 박탈 완료".format(rows_updated))
    disallow_g3.short_description = "권한 박탈: G3"

    def allow_g4(self, request, queryset):
        rows_updated = queryset.update(permission_g4=True)
        self.message_user(request, "{}명 G4 사용 권한 부여 완료".format(rows_updated))
    allow_g4.short_description = "권한 부여: G4"

    def disallow_g4(self, request, queryset):
        rows_updated = queryset.update(permission_g4=False)
        self.message_user(request, "{}명 G4 사용 권한 박탈 완료".format(rows_updated))
    disallow_g4.short_description = "권한 박탈: G4"

    def allow_mypage(self, request, queryset):
        rows_updated = queryset.update(permission_mypage=True)
        self.message_user(request, "{}명 My Page 사용 권한 부여 완료".format(rows_updated))
    allow_mypage.short_description = "권한 부여: My Page"

    def disallow_mypage(self, request, queryset):
        rows_updated = queryset.update(permission_mypage=False)
        self.message_user(request, "{}명 My Page 사용 권한 박탈 완료".format(rows_updated))
    disallow_mypage.short_description = "권한 박탈: My Page"

    def comment_link(self, obj):
        return format_html(
            """
            <select onchange="location = this.value;">
                <option disabled selected value> --------- </option>
                <option value="{}?target_user_id={}">G1&nbsp;</option>
                <option value="{}?target_user_id={}">G1 RoundResult&nbsp;</option>
                <option value="{}?target_user_id={}">G2 golf swing&nbsp;</option>
                <option value="{}?target_user_id={}">G2 short game&nbsp;</option>
                <option value="{}?target_user_id={}">G2 putting&nbsp;</option>
                <option value="{}?target_user_id={}">G3&nbsp;</option>
                <option value="{}?target_user_id={}">G4&nbsp;</option>
            </select>
            """,
            reverse('g1_profile'), obj.user.username,
            reverse('g1_round'), obj.user.username,
            reverse('g2_eval_golf_swing'), obj.user.username,
            reverse('g2_eval_short_game'), obj.user.username,
            reverse('g2_eval_putting'), obj.user.username,
            reverse('g3_profile'), obj.user.username,
            reverse('g4_profile'), obj.user.username,
        )
    comment_link.allow_tags = True

    list_per_page = 20
    fieldsets = [
        ('기본 정보', {'fields': ['user']}),
        ('회원 정보', {'fields': ['full_name', 'email', 'sex', 'birth', 'association', 'handicap']}),
        ('권한', {'fields': ['permission_g1', 'permission_g2', 'permission_g3', 'permission_g4',
                           'permission_mypage']})
    ]

    list_display = ('user', 'full_name', 'association', 'comment_link',
                    'permission_g1', 'permission_g2', 'permission_g3', 'permission_g4', 'permission_mypage')
    list_editable = ('permission_g1', 'permission_g2', 'permission_g3', 'permission_g4', 'permission_mypage')
    list_filter = ['association']
    search_fields = ['user__username', 'full_name', 'association']
    actions = ['delete_selected',allow_g1, allow_g2, allow_g3, allow_g4, allow_mypage,
               disallow_g1, disallow_g2, disallow_g3, disallow_g4, disallow_mypage]
