from django.urls import re_path
from . import views

app_name = "memos"
urlpatterns =[
    #path("", views.MemoList.as_view(), name="memos_lista"),
    re_path(r'^$', views.MemoList.as_view(), name='list'),
    re_path(r'^(?P<pk>\d+)$', views.MemoDetail.as_view(), name='detail'),
    re_path(r'^nuevo$', views.MemoCreation.as_view(), name='new'),
    re_path(r'^editar/(?P<pk>\d+)$', views.MemoUpdate.as_view(), name='edit'),
    re_path(r'^borrar/(?P<pk>\d+)$', views.MemoDelete.as_view(), name='delete'),
]