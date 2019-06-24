from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import FavoriteThingSerializer
from rest_framework.permissions import IsAuthenticated
from core.custom_permissions import IsObjectOwner
from core.authentication import CookieAuthentication
from core.models import FavoriteThing, Category
from django.db.models import Q
from favorite_thing.helper import reorder_rankings_subtract


class FavoriteThingsList(generics.ListCreateAPIView):
    serializer_class = FavoriteThingSerializer
    authentication_classes = (CookieAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category_id = request.data.get('category')
        category_queryset = Category.objects.filter(pk=category_id)
        category = category_queryset.filter(Q(user=self.request.user) | Q(default=True))
        if not category:
            return Response({
                'category': 'Category unavailable - object not found'
            }, status=status.HTTP_404_NOT_FOUND)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = FavoriteThing.objects.filter(user=self.request.user).order_by('ranking')
        return queryset


class FavoriteThingsDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FavoriteThingSerializer
    authentication_classes = (CookieAuthentication,)
    permission_classes = (IsAuthenticated, IsObjectOwner)

    def get_queryset(self):
        queryset = FavoriteThing.objects.order_by('ranking').filter(user=self.request.user)
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        category = request.data.get('category', '')
        if category:
            category_queryset = Category.objects.filter(pk=category)
            category = category_queryset.filter(Q(user=self.request.user) | Q(default=True))
            if not category:
                return Response({
                    'detail': 'Category unavailable - object not found'
                }, status=status.HTTP_404_NOT_FOUND)

        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_destroy(self, instance):
        queryset = self.get_queryset()
        next_rankings = queryset.filter(Q(ranking__gt=instance.ranking) & Q(category=instance.category))
        reorder_rankings_subtract(next_rankings)
        instance.delete()


class FavoriteThingsInCategory(generics.ListAPIView):
    serializer_class = FavoriteThingSerializer
    authentication_classes = (CookieAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        category_id = kwargs['category_id']
        favorite_things = queryset.filter(category=category_id)
        serializer = self.get_serializer(favorite_things, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = FavoriteThing.objects.order_by('ranking').filter(user=self.request.user)
        return queryset
