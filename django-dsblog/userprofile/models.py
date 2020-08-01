from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save # 一个内置信号，可以在模型调用 save() 方法后发出信号
from django.dispatch import receiver           # 信号接收器的装饰器

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 和 User 模型构成一对一的关系，related_name 参数为反向查找时的别名，
	# 字段中有 related_name 参数时，用该参数的值替代默认的表名 _set
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='user/%Y%m%d/', blank=True) 
    # ImageField 字段不会存储图片本身，而是仅仅保存图片的地址。
    # 头像图片保存在类似 /media/user/20191001/ 的地址中。
    bio = models.TextField(max_length=500, blank=True) # 个人简介

    def __str__(self):
        return 'user {}'.format(self.user.username)


#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)
# 信号接收函数，每当新建 User 实例时自动调用,
# post_save 是一个内置信号，可以在模型调用 save() 方法后发出信号
# 装饰器 receiver 起到接收器的作用，每当User有更新就发送一个信号启动 post_save 相关的函数
# 通过信号的传递，实现了每当 User 创建/更新时，Profile也会自动的创建/更新


#@receiver(post_save, sender=User) # 信号接收函数，每当更新 User 实例时自动调用
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()