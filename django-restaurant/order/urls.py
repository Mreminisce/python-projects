from django.urls import path

from . import views


app_name = 'order'
urlpatterns = [
    path('desklist/', views.DeskListView.as_view(), name='desklist'),
    path('meallist/', views.MealListView.as_view(), name='meallist'),
    path('orderlist/', views.OrderListView.as_view(), name='orderlist'),
    path('neworder/', views.neworder, name='neworder'),
    path('newmeal/', views.newmeal, name='newmeal'),
    path('newdesk/', views.newdesk, name='newdesk'),
    path('deleteorder/<int:id>/', views.deleteorder, name='deleteorder'),
    path('deletemeal/<int:id>/', views.deletemeal, name='deletemeal'),
    path('deletedesk/<int:id>/', views.deletedesk, name='deletedesk'),
]