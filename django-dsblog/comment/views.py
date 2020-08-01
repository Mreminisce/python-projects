from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from notifications.signals import notify # django-notifications-hq 消息通知库

from article.models import ArticlePost
from .forms import CommentForm
from .models import Comment

# Create your views here.

@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id, parent_comment_id=None):
# parent_comment_id 参数代表父评论的 id 值，None 表示一级评论，具体值表示多级评论
    article = get_object_or_404(ArticlePost, id=article_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二级评论
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)  
                new_comment.parent_id = parent_comment.get_root().id
                # 若评论层级超过二级则转换为二级，get_root() 方法将其父级重置为树形结构最底部的一级评论
                new_comment.reply_to = parent_comment.user
                new_comment.save()

                # 给其他用户发送通知，不给管理员和自己通知
                if not parent_comment.user == request.user:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )

                return JsonResponse({"code": "200 OK", "new_comment_id": new_comment.id})

            new_comment.save()  

            # 给管理员发送通知
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='评论了你',
                    target=article,
                    action_object=new_comment,
                )

            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
            return redirect(redirect_url)
            # 如果参数是一个 Model 对象则自动调用这个对象的 get_absolute_url() 方法查询某篇文章的地址
        else:
            return HttpResponse('表单内容有误，请重新填写')
    elif request.method == 'GET':
        comment_form = CommentForm()

        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }

        return render(request, 'comment/reply.html', context)
    else:
        return HttpResponse('仅接受 GET 和 POST 请求发表评论')