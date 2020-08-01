"""dsblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from article.views import article_list

import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', article_list, name='home'),
    path('article/', include('article.urls', namespace='article')),
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('comment/', include('comment.urls', namespace='comment')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    # 为了确保模块安装到正确的命名空间中这里的 notifications.urls 没有像之前一样用字符串
    path('notice/', include('notice.urls', namespace='notice')),
    # path('accounts/', include('allauth.urls')),
]
# namespace 可以保证反查到唯一的 URL (即使不同的 APP 使用相同的 URL)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)