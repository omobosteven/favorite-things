from django.db.models import Q
from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core.authentication import CookieAuthentication
from core.models import Category, CategoryUser
from .serializers import CategorySerializer


class CreateListCategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    authentication_classes = (CookieAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data = {'name': request.data.get('name', '').lower()}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get('name')

        is_default = Category.objects.filter(
            Q(name=name) & Q(default=True)).values()
        if is_default:
            return Response({
                'message': 'Category already exist'
            }, status=status.HTTP_409_CONFLICT)

        if Category.objects.filter(name=name):
            try:
                existing_category = Category.objects.get(name=name)
                CategoryUser.objects.create(
                    user=self.request.user, category=existing_category)
                return Response({
                    'message': 'Category added successfully'
                }, status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({
                    'message': 'Category already exist'
                }, status=status.HTTP_409_CONFLICT)

        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = Category.objects.filter(
            Q(default=True) | Q(user=self.request.user))
        return queryset
