from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from snippets import view_sets

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', view_sets.SnippetViewSet)
router.register(r'users', view_sets.UserViewSet)

# Routerを指定するパターン
urlpatterns = [
    url(r'^', include(router.urls))
]

# Routerを使う場合は、以下がいらないのか？
# https://github.com/encode/django-rest-framework/issues/1337
# urlpatterns = format_suffix_patterns(urlpatterns)
