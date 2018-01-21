from rest_framework import serializers
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    """シリアライザクラス"""

    # シリアライズ/デシリアライズされるフィールドの定義
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)

    # styleで指定しているのは、DjangoのFormで「widget=widgets.Textarea】するのと同じ
    code = serializers.CharField(style={'base_template': 'textarea.html'})

    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        # serializers.Serializerのメソッドをオーバーライド
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # こちらも、serializers.Serializerのメソッドをオーバーライド

        # validated_dataとは？
        # get()の第一引数と、第二引数の意味は？
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)

        # ここまでの情報で、どれだけの情報を持ったインスタンスが変更されるかが決まる
        instance.save()
        return instance


class SnippetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        # Modelのうち、必要なフィールドをタプルとして用意
        # チュートリアルとは異なり、styleを削ってみる
        fields = ('id', 'title', 'code', 'linenos', 'language',)
