from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.reverse import reverse

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


# APIのルート
@api_view(['GET', ])
def api_root(request, format=None):
    return Response({
        # 完全修飾URLを返すために、reverse関数を使う
        # 'user-list'などの名前をつけた場合は、urls.pyでもname引数を指定しないとエラーで動作しなくなる
        'users': reverse('user-list', request=request, format=format),
        'snippet': reverse('snippet-list', request=request, format=format),
    })


# CSRFトークンを持たないクライアントからビューにPOSTできるようにするためのデコレータ
@csrf_exempt
def snippet_list(request):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        # Djangoモデルをシリアライズする
        serializer = SnippetSerializer(snippets, many=True)
        # Jsonとして返すため、dict型の`serializer.data`を、JsonResponseに渡す
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        # リクエスト(ストリーム)を、Pythonネイティブのdict型に変換する
        data = JSONParser().parse(request)
        # Djangoのデータモデルにする
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            # 問題なければ保存する
            serializer.save()
            # dict型のデータ(serializer.data)をJSONとして返す
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        # 問題あれば、400として返す
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# リファクタリング後
@api_view(['GET', 'POST'])
def snippet_list_2nd(request, format=None):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        # @api_viewを使うことで、DjangoのJsonResponseではなく
        # rest_frameworkのResponseが使えるようになる
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def snippet_detail(request, pk):
    # 個々のsnippetに対するビュー
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# リファクタリング後
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail_2nd(request, pk, format=None):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
