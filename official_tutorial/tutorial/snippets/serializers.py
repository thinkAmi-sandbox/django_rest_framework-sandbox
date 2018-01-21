from rest_framework import serializers
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


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
    # 引数source：フィールドにセットされる値を制御する
    # シリアライズされた任意の属性を指定できる
    # ReadOnlyFieldは読み取り専用：デシリアライズされた時にモデルインスタンスを更新することはない
    # (今回のケースなら、"CharField(read_only=True)"も使える
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        # Modelのうち、必要なフィールドをタプルとして用意
        # チュートリアルとは異なり、styleを削ってみる
        # ownerというReadOnlyFieldを追加したので、fieldとして扱えるよう、ownerを加える
        fields = ('id', 'title', 'code', 'linenos', 'language', 'owner')


class UserSerializer(serializers.ModelSerializer):
    # リバースリレーションシップなため、ModelSerializerを使うだけでは、デフォルトではフィールドに含まれない
    # そのため、明示的にフィールドを追加する必要がある
    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        # Userモデルの持っているid, usernameの他、上で定義したsnippetsもフィールドとして有効化
        fields = ('id', 'username', 'snippets')


# HyperlinkedModelSerializerを使って、エンティティ間の関連を表す
class SnippetHyperLinkedSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # formatがhtmlなため、highlightではどんなフォーマットが指定されても
    # `.html` suffixが指定されたものとして、動作させる必要がある
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


class UserHyperLinkedSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')
