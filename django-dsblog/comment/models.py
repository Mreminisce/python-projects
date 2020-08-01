from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField # django-ckeditor 库
from mptt.models import MPTTModel, TreeForeignKey # django-mptt 库

from article.models import ArticlePost

# Create your models here.

class Comment(MPTTModel):
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = RichTextField()
    created_time = models.DateTimeField(auto_now_add=True)
    
    parent = TreeForeignKey( 
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    # mptt 树形结构，parent 字段用于存储数据之间的关系，必须定义

    
    reply_to = models.ForeignKey( # 被评论人字段
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    class MPTTMeta:
        order_insertion_by = ['created_time']
    # 替换 Meta 为 MPTTMeta，模型会自动添加几个用于树形算法的新字段

    def __str__(self):
        return self.body[:20]