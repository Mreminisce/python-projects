from django.urls import path
from . import views


app_name = 'comment'
urlpatterns = [
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
    # 一级评论没有 parent_comment_id 参数，因此视图使用缺省值 None，实现了区分评论层级
    path('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply')
    # 二级评论
]