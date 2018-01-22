from django.conf.urls import re_path, include
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from snippets import class_views
from snippets import generic_views
from snippets import mixin_views
from snippets import views
from .view_sets import SnippetViewSet, UserViewSet

# ViewSetを実際のクラスに割り当てるための変数
snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

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
    # APIのルートで、このURLを `snippet-list` として参照している
    re_path(r'^snippets5/$', generic_views.SnippetList.as_view(),
            name='snippet-list'),
    # Serializerに'url'フィールドがあり、デフォルトで'{model_name}-detail'を参照するためnameに設定
    re_path(r'^snippets5/(?P<pk>[0-9]+)/$', generic_views.SnippetDetail.as_view(),
            name='snippet-detail'),

    # User用のview
    # APIのルートで、このURLを `user-list` として参照している
    re_path(r'^users/$', generic_views.UserList.as_view(),
            name='user-list'),
    # Serializerに'url'フィールドがあり、デフォルトで'{model_name}-detail'を参照するためnameに設定
    # また、UserSerializerから参照されていることにも注意
    re_path(r'^users/(?P<pk>[0-9]+)/$', generic_views.UserDetail.as_view(),
            name='user-detail'),

    # APIのルート (非ジェネリックなviewで作成している)
    # re_path(r'^$', views.api_root),

    # シンタックスハイライトのある、静的なHTMLをレンダリングするURL
    # SnippetSerializerから参照されている
    re_path(r'^snippets5/(?P<pk>[0-9]+)/highlight/$', generic_views.SnippetHighlight.as_view(),
            name='snippet-highlight'),

    # ViewSetを使った手動ルーティング
    re_path(r'^snippets6/$', snippet_list, name='snippet-list'),
    re_path(r'^snippets6/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
    re_path(r'^snippets6/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
    re_path(r'^users6/$', user_list, name='user-list'),
    re_path(r'^users6/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
]

# フォーマットsuffix を使えるように設定する
urlpatterns = format_suffix_patterns(urlpatterns)

# ブラウザ用のログインビュー・ログアウトビューを追加
urlpatterns += [
    # Django1.9以降の場合、include()のnamespaceは自動設定されるので
    # `namespace=rest_framework` のように明示的に設定する必要はなくなった
    re_path(r'^api-auth/', include('rest_framework.urls'))
]

