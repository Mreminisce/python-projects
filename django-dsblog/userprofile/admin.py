from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile

# Register your models here.

class ProfileInline(admin.StackedInline): # 定义一个行内 admin
    model = Profile
    can_delete = False
    verbose_name_plural = 'UserProfile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)           # 将 Profile 表格合并到 User 表格中


admin.site.unregister(User)               # 重新注册 User
admin.site.register(User, UserAdmin)