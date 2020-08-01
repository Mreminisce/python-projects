from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserLoginForm(forms.Form):         # 适用于不与数据库进行直接交互的表单
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(forms.ModelForm): # 适用于需要对数据库进行操作的表单,可以自动生成模型中已有的字段
    password = forms.CharField()         # 覆写 password 字段
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')
        # Meta 中的定义对覆写后的某字段没有效果，因此 fields 不用包含 password

    def clean_password2(self): # def clean_[字段] 方法会被自动调用，用来对单个字段的数据进行验证清洗
        data = self.cleaned_data

        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('两次密码输入不一致，请重试')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')