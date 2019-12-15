"""mp3converter URL Configuration"""

from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from converter.views import ConvertedFileViewSet, FileInfoViewSet, CoverImageViewSet
from rest_framework import routers
from converter.myrouters import InfoRouter, CoverRouter

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'converter', FileInfoViewSet, 'converter')
cover_router = CoverRouter()
info_router = InfoRouter()
info_router.register(r'file', ConvertedFileViewSet, 'file')
cover_router.register(r'file', CoverImageViewSet, 'file')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', obtain_auth_token, name='api_token_auth'),
]
urlpatterns += router.urls
urlpatterns += info_router.urls
urlpatterns += cover_router.urls