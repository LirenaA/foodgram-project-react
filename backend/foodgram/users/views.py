from django.shortcuts import render
from rest_framework import status, viewsets
from users.models import CustomUser, Follow
from api.permissions import CustomUserPermissions, IsAuthor, IsAuthorOrReadOnly, CanViewAnyObject
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers import UserSerializer, PasswordSerializer

class CustomUserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post', 'delete']

    @action(
        detail=False, methods=['get'],
        url_name='me', url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def current_user_information(self, request):
        return Response(
            UserSerializer(request.user).data,
            status=status.HTTP_200_OK
        )
    
    @action(
        detail=False, methods=['post'],
    )
    def set_password(self, request):
        user = get_object_or_404(CustomUser, username=request.user)
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(serializer.data['current_password']):
            return Response({'status': 'Текущий пароль указан неверно'})
        user.set_password(serializer.data['new_password'])
        user.save()
        return Response(
            {'status': 'Пароль изменен'},
            status=status.HTTP_204_NO_CONTENT
        )
        
    @action(
        detail=False,
        permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        queryset = Subscribe.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request},)
        return self.get_paginated_response(serializer.data)