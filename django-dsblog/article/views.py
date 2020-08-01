import markdown
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required # 验证登录装饰器
from django.core.paginator import Paginator               # 分页模块
from django.db.models import Q                            # Q 对象
from django.http import HttpResponse
from django.views import View # 类视图

from .forms import ArticlePostForm
from .models import ArticlePost, ArticleColumn
from comment.models import Comment
from comment.forms import CommentForm

# Create your views here.

def article_list(request):
    search = request.GET.get('search') # search 参数存放需要搜索的文本，检索特定的文章对象
    order = request.GET.get('order')   # 从 url 中提取查询参数
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    article_list = ArticlePost.objects.all()
  
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) | Q(body__icontains=search) # 
        )
    else:
        search = ''
    # 用 Q 对象进行联合搜索，Q(title__icontains=search) 中 title 是要查询的模型字段，icontains 
    # 是不区分大小写的包含，对应 contains 是区分大小写的包含；中间用双下划线 __ 隔开，多个 Q 对象
    # 用管道符 | 隔开，这样就实现了联合查询。
    # 若没有接收到 search 参数就将其设置为空字符串，避免模板错误地传递 'search = None'

    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])
        # 在 tags 字段中过滤 name 为 tag 的数据条目
        # django-taggit 库还支持多标签的联合查询：tags__name__in=["tag1", "tag2"]

    if order == 'total_views': # 根据 GET 请求中不同的查询条件返回不同的排序结果
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 3) # 每页显示 3 篇文章
    page = request.GET.get('page')         # 获取 url 中的页码
    articles = paginator.get_page(page)    # 将导航对象相应的页码内容返回给 articles

    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    } # 需要传递给模板的上下文变量

    return render(request, 'article/list.html', context)
    # 结合模板和上下文变量返回渲染后的 HttpResponse 对象


def article_detail(request, id): # id: 模型自动生成的主键
    article = get_object_or_404(ArticlePost, id=id)
    article.total_views += 1
    article.save(update_fields=['total_views']) 
    # update_fields=[] 指定数据库只更新 total_views 字段，优化执行效率
    comments = Comment.objects.filter(article=id)
    # filter 可以取出多个满足条件的对象，get 只能取出1个

    md = markdown.Markdown(
        extensions=[ # 载入常用的语法扩展
            'markdown.extensions.extra',  
            'markdown.extensions.codehilite', 
            'markdown.extensions.toc', # Table Of Contents
        ]
    )
    article.body = md.convert(article.body)
    # 注意 markdown.markdown() 和 markdown.Markdown() 的区别，详细的解释见官方文档
    # 先将 Markdown 类赋值给一个临时变量 md，然后用 convert() 方法将需要渲染的文章正文
    # article.bode 渲染为 html 页面，再通过 md.toc 将目录传递给模板

    comment_form = CommentForm()
    context = { 
        'article': article,
        'toc': md.toc,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'article/detail.html', context)


@login_required(login_url='userprofile/login/')
def article_create(request):
    if request.method == "POST": # 判断用户是否是以 POST 方法提交表单数据
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 将提交的数据赋值到表单实例中

        if article_post_form.is_valid():                        # 判断提交数据是否满足表单的要求
            new_article = article_post_form.save(commit=False)  # 保存数据，但不提交到数据库中
            new_article.author = User.objects.get(id=request.user.id) # 指定文章作者

            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 判断文章是否已经有分类，若有则根据表单提交的 value 值关联对应的分类

            new_article.save()                                  # 将新文章保存到数据库中
            article_post_form.save_m2m()
            # 如果表单提交时用了 commit=False 选项就必须用 save_m2m() 方法来保存标签的多对多关系

            return redirect('article:article_list')             # 完成后返回到文章列表
        else:
            return HttpResponse('表单内容有误，请重新填写')
    
    else:
        article_post_form = ArticlePostForm() # 如果用户是 GET 请求方法则返回一个空的表单类对象
        columns = ArticleColumn.objects.all()
        context = {'article_post_form': article_post_form, 'columns': columns} # 上下文参数

        return render(request, 'article/create.html', context)


@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.user != article.author:
        return HttpResponse('没有权限删除此文章')

    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id) # 根据 id 获取需要删除的文章
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('只允许 POST 方法请求')


@login_required(login_url='/userprofile/login/') # 过滤未登录的用户
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)

    if request.user != article.author:
        return HttpResponse('没有权限修改此文章')

    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)

        if article_post_form.is_valid():                     # 保存新写入的 title、body 数据
            article.title = request.POST['title']
            article.body = request.POST['body']

            if request.POST['column'] != 'None':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None

            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')

            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            # tags.set() 和 tags.names() 都是 taggit 库提供的接口，分别用于更新数据和获取标签名
            article.save()
            return redirect('article:article_detail', id=id) # 返回到修改后的文章页面中
        else:
            return HttpResponse('表单内容有误，请重新填写')
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()

        context = {
            'article': article, 
            'article_post_form': article_post_form,
            'columns': columns,
            'tags': ','.join([x for x in article.tags.names()]), # 用列表生成器将数据转换为字符串
        }
        # 赋值上下文，将 article 文章对象也传递进去以便提取旧的内容

        return render(request, 'article/update.html', context) # 将响应返回到模板中


class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')