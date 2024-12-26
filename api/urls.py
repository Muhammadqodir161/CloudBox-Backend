from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LogoutView, FolderViewSet, FileViewSet

router = DefaultRouter()
router.register('folders', FolderViewSet, basename='folders')
router.register('files', FileViewSet, basename='files')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]

