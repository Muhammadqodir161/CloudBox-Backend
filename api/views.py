from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, status
from .models import File, Folder
from .pagination import CustomPagination
from .serializers import FileSerializer, FolderSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if User.objects.filter(username=email).exists():
            return Response({"error": "Email allaqachon mavjud"}, status=400)
        user = User.objects.create_user(username=email, email=email, password=password)
        return Response({"message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi", "userId": user.id})

class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "Muvaffaqiyatli chiqish amalga oshirildi"})

class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    pagination_class = CustomPagination
    filterset_fields = ['folder', 'name']  
    search_fields = ['name']             
    ordering_fields = ['uploaded_at', 'name']  
    ordering = ['uploaded_at']            

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class FolderViewSet(viewsets.ModelViewSet):
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['parent']         
    search_fields = ['name']             

    def get_queryset(self):
        return Folder.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)