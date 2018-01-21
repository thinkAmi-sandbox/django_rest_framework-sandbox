from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics


# 先ほどまでのMixinが全て入っているgeneric view
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
