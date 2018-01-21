from django.conf.urls import re_path
from snippets import views
from snippets import class_views
from snippets import mixin_views
from snippets import generic_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # Django 2.0からはurlではなく、re_path()に変わった
    # https://docs.djangoproject.com/en/2.0/ref/urls/#url
    re_path(r'^snippets/$', views.snippet_list),
    re_path(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
    # リファクタリングしたあと
    re_path(r'^snippets2/$', views.snippet_list_2nd),
    re_path(r'^snippets2/(?P<pk>[0-9]+)/$', views.snippet_detail_2nd),
    # クラスベースviewを使ったもの
    re_path(r'^snippets3/$', class_views.SnippetList.as_view()),
    re_path(r'^snippets3/(?P<pk>[0-9]+)/$', class_views.SnippetDetail.as_view()),
    # mixin view を使ったもの
    re_path(r'^snippets4/$', mixin_views.SnippetList.as_view()),
    re_path(r'^snippets4/(?P<pk>[0-9]+)/$', mixin_views.SnippetDetail.as_view()),
    # generic view を使ったもの
    re_path(r'^snippets5/$', generic_views.SnippetList.as_view()),
    re_path(r'^snippets5/(?P<pk>[0-9]+)/$', generic_views.SnippetDetail.as_view()),
]

# フォーマットsuffix を使えるように設定する
urlpatterns = format_suffix_patterns(urlpatterns)
