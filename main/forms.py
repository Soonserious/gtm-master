# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, password_validation
from . import models
from django.utils.safestring import mark_safe


# class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    # def render(self):
        # return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class SignUpUserForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': "비밀번호가 일치하지 않습니다.",
    }

    username = forms.RegexField(
        label='아이디',
        max_length=30,
        regex=r'^[\w.-]+$',
        error_messages={
            'invalid': "ID는 알파벳이나 숫자 또는 '.', '-', '_' 문자로만 이루어져야 합니다."
        },
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required': 'True',
            }
        ),
    )
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'required': 'True',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(SignUpUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        if commit:
            user.save()
        return user


class SignUpMemberForm(forms.ModelForm):

    birth = forms.DateField(input_formats=['%Y%m%d'], required=False)

    class Meta:
        model = models.Member
        fields = ('full_name', 'sex', 'association', 'handicap', 'email', 'phone_number', 'birth')


class SignInForm(AuthenticationForm):

    username = forms.RegexField(
        label=u'아이디',
        max_length=30,
        regex=r'^[\w.-]+$',
        error_messages={
            'invalid': "ID는 알파벳이나 숫자 또는 '.', '-', '_' 문자로만 이루어져야 합니다."
        },
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required': 'True',
            }
        ),
    )
    password = forms.CharField(
        label=u'비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'required': 'True',
            }
        )
    )

    error_messages = {
        'non_exist_id': "아이디가 존재하지 않습니다.",
        'wrong_pw': "비밀번호가 틀렸습니다.",
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['non_exist_id'],
                    code='non_exist_id',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                if self.user_cache.check_password(password):
                    pass
                else:
                    raise forms.ValidationError(
                        self.error_messages['wrong_pw'],
                        code='wrong_pw',
                    )

        return self.cleaned_data


class AccountForm(forms.Form):

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput
    )
