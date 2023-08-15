from api.paginations import PageNumberCustomPagination
from api.serialiazers import SubscriberSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = PageNumberCustomPagination

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
        serializer_class=SubscriberSerializer
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        is_following = request.user.follower.filter(author=author)
        if is_following:
            if request.method == 'POST':
                return Response(status=status.HTTP_400_BAD_REQUEST)

            is_following.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == 'DELETE':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request.user.follower.create(author=author)
        return Response(
            self.get_serializer(author).data,
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=False,
        methods=['get'],
        serializer_class=SubscriberSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(followed__user=request.user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
