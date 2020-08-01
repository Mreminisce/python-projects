from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from .models import Profile

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)

        if user_login_form.is_valid():
            data = user_login_form.cleaned_data # 将各种数据清洗为一致的输出
            user = authenticate(username=data['username'], password=data['password'])
            # 检验用户名和密码是否在数据库中正确匹配，如果匹配则返回这个 user 对象

            if user:
                login(request, user)  # 将用户数据保存在 session 中以实现登录

                return redirect('article:article_list')
            else:
                return HttpResponse('账号或密码输入错误，请重新输入')
        else:
            return HttpResponse('账号或密码输入不合法')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'user_login_form': user_login_form}

        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse('必须使用 GET 或 POST 方法请求数据')


def user_logout(request):
    logout(request)

    return redirect('userprofile:login')


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)

        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('article:article_list')
        else:
            return HttpResponse('注册表单输入有误，请重新输入')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse('必须使用 GET 或者 POST 方法请求数据')


@login_required(login_url='/userprofile/login/')
# 验证登录的装饰器，要求调用函数时用户必须登录；如果未登录则不执行函数并将页面重定向到指定页面
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        if request.user == user:
            logout(request)
            user.delete() # 先退出登录后删除数据
            return redirect('article:article_list')
        else:
            return HttpResponse('没有权限进行删除操作')
    else:
        return HttpResponse('仅接受 POST 方法请求')


@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    
    if Profile.objects.filter(user_id=id).exists():
        # user_id 是 OneToOneField 自动生成的字段，用来表征两个数据表的关联
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)
        # 如果 Profile 表格已经存在就获取其中的数据，不存在就新建一个
      
    if request.method == 'POST':
        if request.user != user:
            return HttpResponse('没有权限修改此用户信息')

        profile_form = ProfileForm(request.POST, request.FILES)
        # 表单上传的文件存储在类字典对象 request.FILES 中，通过参数一并传递给表单类

        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data # 取得清洗后的合法数据
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']

            if 'avatar' in request.FILES: # 如果 request.FILES 存在文件，则赋值给 profile.avatar 保存
                profile.avatar = profile_cd['avatar']

            profile.save()

            return redirect('userprofile:edit', id=id) # 带参数的 redirect() 方法
        else:
            return HttpResponse('注册表单输入有误，请重新输入')

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'profile': profile, 'user': user}
        # 其实 GET 方法不需要将 profile_form 表单对象传递到模板中去，
        # 因为模板中已经用 Bootstrap 写好了表单，实际上 profile_form 表单对象并没有用到
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse('必须使用 GET 或者 POST　方法请求数据')