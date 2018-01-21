from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics
# UserList, UserDetailのために追加
from django.contrib.auth.models import User
from .serializers import UserSerializer
# パーミッションのために追加
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
# あらかじめレンダリングされたHTMLを表示するために使う
from rest_framework import renderers
from rest_framework.response import Response


# 先ほどまでのMixinが全て入っているgeneric view
class SnippetList(generics.ListCreateAPIView):
    # querysetには、データソースとなるクエリセットを指定
    queryset = Snippet.objects.all()
    # serializer_classには、シリアライザクラスを指定
    serializer_class = SnippetSerializer
    # パーミッションを設定：権限なければ読み取り専用
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        # リクエストに含まれるユーザを、Snippetシリアライザで保存する時に渡す
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # パーミッションを設定：権限なければ読み取り専用
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


# Userモデルは読み取り専用のビューとしたい
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# シンタックスハイライトを行うView
# getメソッドをオーバーライドして、任意の値(ここではオブジェクトリストの属性)を返している
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
