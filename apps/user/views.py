import json
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, mixins, status, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.serializers import RegisterSerializer, LoginSerializer, \
    UserDetailsSerializer, JWTSerializer, PasswordChangeSerializer, UserProfileSerializer
from user.models import User, Profile
from utils.pagination import SmallResultsSetPagination


def jwt_encode(user):
    try:
        from rest_framework_jwt.settings import api_settings
    except ImportError:
        raise ImportError("djangorestframework_jwt needs to be installed")

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.none()

    def get_serializer_class(self):
        if self.action == 'registration':
            return RegisterSerializer
        elif self.action == 'login':
            return LoginSerializer
        elif self.action == 'change_password':
            return PasswordChangeSerializer
        return UserDetailsSerializer

    @action(['post'], detail=False, permission_classes=[permissions.AllowAny])
    def registration(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 检查手机号是否已经被注册
        user_check = User.objects.filter(mobile=serializer.data['mobile']).count()
        if user_check:
            return JsonResponse({"code": 400, "message": "该手机号已注册！"},
                                status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save(self.request)
        token = jwt_encode(user)

        data = {
            'user': user,
            'token': token
        }
        response_data = JWTSerializer(data).data

        return Response(response_data,
                        status=status.HTTP_201_CREATED)

    @action(['post'], detail=False, permission_classes=[permissions.AllowAny])
    @csrf_exempt
    def login(self, request):
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token = jwt_encode(user)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_login(request, user)

        user.username = user.mobile
        user.first_name = ''
        # 获取用户基本信息
        user_profile = Profile.objects.filter(user=user)
        if user_profile.count() > 0:
            user.username = user_profile[0].name
            user.first_name = user_profile[0].avatar

        data = {
            'user': user,
            'token': self.request.session._SessionBase__session_key,
        }
        response_serializer = JWTSerializer(data, context={'request': self.request})
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(['post'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        django_logout(request)

        return Response({"detail": "退出登录成功"},
                        status=status.HTTP_200_OK)

    @action(['get'], detail=False,
            permission_classes=[permissions.IsAuthenticated],
            url_path='detail', url_name='user-detail')
    def detail_info(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(['post'], detail=False, permission_classes=[permissions.IsAuthenticated],
            url_path='change-password', url_name='change-password')
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "密码修改成功"})


class UserProfileViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user_id',)
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()

    def list(self, request, *args, **kwargs):
        if isinstance(self.request.user, AnonymousUser):
            return Response({"detail": "需要登录"}, status=status.HTTP_401_UNAUTHORIZED)
        query_set = Profile.objects.filter(user=self.request.user)
        if query_set.count():
            serializer = self.get_serializer(query_set[0])
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': '没有找到用户信息'}, status=status.HTTP_404_NOT_FOUND)
