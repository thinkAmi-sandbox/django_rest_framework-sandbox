from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # このパーミッションはBasic認証のものっぽい
        # HTTPメソッドが GET, HEAD, OPTIONS の場合は権限あり
        if request.method in permissions.SAFE_METHODS:
            return True

        # それ以外のHTTPメソッドの場合は、オブジェクトのオーナーが
        # リクエストしたユーザであれば権限ありとする
        return obj.owner == request.user
