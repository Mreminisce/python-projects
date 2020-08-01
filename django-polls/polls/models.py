from django.db import models
from django.utils import timezone
import datetime
# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Published Date') # 可选的第一位置参数，设置更好可读性的的字段名

    # 添加__str__方法，在 print 或者 Admin 后台展示对象时显示更直观的信息，而不是只是一个对象类型名称
    def __str__(self): 
        return self.question_text

    # 判断问卷是否是最近时间段内发布的
    def was_published_recently(self):
        now = timezone.now()
        # timedelta 对象表示两个 date 或者 time 的时间间隔
        return now - datetime.timedelta(days=1) <= self.pub_date <=now
    
    # 改进 was_published_recently 属性在 Admin 后台输出的样式
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_descripttion = 'Published recently ?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # 定义外键关系
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text