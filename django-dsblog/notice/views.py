from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin # 混入类

from article.models import ArticlePost

# Create your views here.

class CommentNoticeListView(LoginRequiredMixin, ListView):
    # 混入类 LoginRequiredMixin 要求调用此视图必须先登录
    context_object_name = 'notices' # 上下文的名称 
    template_name = 'notice/list.html' # 模板位置   
    login_url = '/userprofile/login/' # 登录重定向
  
    def get_queryset(self): # 返回传递给模板的未读通知上下文对象的查询集
        return self.request.user.notifications.unread() # unread()方法用于获取所有未读通知的集合


class CommentNoticeUpdateView(View): # 更新通知状态
    def get(self, request): # 处理 get 请求       
        notice_id = request.GET.get('notice_id') # 获取未读消息
       
        if notice_id: # 判断更新一条还是所有未读通知
            article = ArticlePost.objects.get(id=request.GET.get('article_id'))
            request.user.notifications.get(id=notice_id).mark_as_read() # 将未读通知转换为已读

            return redirect(article)      
        else:
            request.user.notifications.mark_all_as_read()

            return redirect('notice:list')