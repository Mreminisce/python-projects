from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

# Create your views here.
class IndexView(generic.ListView): # 使用通用视图 ListView 显示一个对象的列表
    template_name = 'polls/index.html' # 替换自动生成的默认模板名 <app name>/<model name>_list.html
    context_object_name = 'latest_question_list' # 覆盖自动生成的上下文变量 question_set

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5] # 返回最近发布的5个问题


class DetailView(generic.DetailView): # 通用视图 DetailView 显示特定类型对象的详细页面
    model = Question # 使用模型自动选择合适的上下文变量
    template_name = 'polls/detail.html'        


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    # 如果对象不存在则弹出Http404错误，模型作为第一位置参数，后面可以带任意个关键字参数。
    question = get_object_or_404(Question, pk=question_id) # pk = primary key

    try:
        # choice_set: 内置属性
        # request.POST类似字典，通过键名以string字符串形式返回数据。下面是返回被选择选项的ID
        # 可以改成 request.POST['choice',None] 防止发生异常
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You did not select a choice yet.',
        }) # 字典参数中的数据将传递给模板，最后返回渲染后的HttpResponse对象
    else: # 在 try 没有捕获任何异常的时候执行
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # 使用reverse()函数避免在视图函数中硬编码URL