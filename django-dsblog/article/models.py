from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User # 内建的 User 模型

from taggit.managers import TaggableManager # Django-taggit 标签库
from PIL import Image

# Create your models here.


class ArticleColumn(models.Model): # 文章的分类
    title = models.CharField(max_length=100, blank=True)
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 指定数据删除的方式
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)           # 每次数据更新时自动写入当前时间
    total_views = models.PositiveIntegerField(default=0)        # 存储正整数
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )
    tags = TaggableManager(blank=True)
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    likes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-created_time',)  # 只包含一个元素的元组要在末尾添加逗号

    def __str__(self):                 # 对象 str() 方法的返回值，即对象数据的显示内容
        return self.title

    def get_absolute_url(self):        # 获取文章地址并返回文章详情页面，实现了路由重定向
        return reverse('article:article_detail', args=[self.id])

    def save(self, *args, **kwargs):   # 保存时处理图片
        article = super(ArticlePost, self).save(*args, **kwargs)
        # 调用父类中原有的 save() 方法，将 model 中的字段数据保存到数据库中

        if self.avatar and not kwargs.get('update_fields'): 
        # 处理图片，固定宽度缩放图片大小
        # 不处理没有标题图的文章
        # 'update_fields' 排除统计浏览量时所调用的 save() 方法，以免每次进入文章详情页面都执行图片处理
            image = Image.open(self.avatar) 
            (x, y) = image.size                                           # 取得分辨率
            new_x = 300
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS) # 采用平滑滤波缩放
            resized_image.save(self.avatar.path)                          # 覆盖原图片

        return article