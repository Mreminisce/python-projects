from django.contrib import admin

from .models import Question, Choice

# Register your models here.
class ChoiceInline(admin.TabularInline): # 表格式显示，tabular: 表格的
    model = Choice
    extra = 3 # 设置默认提供3个Choice对象的编辑区域。


class QuestionAdmin(admin.ModelAdmin): # 创建一个继承admin.ModelAdmin的模型管理类来自定义Question
    fieldsets = [
        ('Question Information', {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # 字段集合fieldsets中每一个元组的第一个元素是该字段集合的标题
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date'] # 对显示结果进行过滤
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
# 注册Question模型