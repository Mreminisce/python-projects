from django.urls import path

from . import views

app_name = 'article'
urlpatterns = [
    path('article-list/', views.article_list, name='article_list'), 
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    path('article-create/', views.article_create, name='article_create'),
    path('article-update/<int:id>/', views.article_update, name='article_update'),
    path(
        'article-safe-delete/<int:id>',
        views.article_safe_delete,
        name='article_safe_delete'
    ),
    path(
        'increase-likes/<int:id>/', 
        views.IncreaseLikesView.as_view(), 
        name='increase_likes'
    ),
    
    # name 参数用于反查 url 地址，作为参数传递给模板的 {% url 'app_name:name' %} 标签
]