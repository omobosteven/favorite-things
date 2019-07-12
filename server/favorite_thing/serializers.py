from django.db.utils import IntegrityError
from django.db.models import Q
from rest_framework import serializers
from core.models import FavoriteThing
from core.models import Category
from .helper import reorder_rankings, reorder_rankings_subtract


class FavoriteThingSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='name')

    class Meta:
        model = FavoriteThing
        fields = ('favorite_thing_id', 'title', 'description', 'ranking',
                  'metadata', 'category', 'user', 'created_at', 'modified_at')
        read_only_fields = (
            'favorite_thing_id', 'user', 'created_at', 'modified_at')
        extra_kwargs = {
            'description': {'required': False, 'min_length': 10},
        }

    def create(self, validated_data):
        ranking = validated_data.get('ranking')
        category = validated_data.get('category')
        user = validated_data.get('user')

        rankings_queryset = FavoriteThing.objects.order_by('ranking')\
            .filter(Q(category=category) & Q(user=user.user_id))
        existing_ranking = rankings_queryset.filter(ranking=ranking)

        if not rankings_queryset and ranking > 1:
            ranking = 1
            validated_data = {**validated_data, 'ranking': ranking}

        if rankings_queryset and \
                ranking > rankings_queryset.last().ranking + 1:
            ranking = rankings_queryset.last().ranking + 1
            validated_data = {**validated_data, 'ranking': ranking}

        if existing_ranking:
            next_rankings = rankings_queryset.filter(ranking__gte=ranking)
            reorder_rankings(next_rankings)

        try:
            favorite_thing = FavoriteThing.objects.create(**validated_data)
            return favorite_thing
        except IntegrityError:
            raise serializers.ValidationError('Favorite thing already exist')

    def update(self, instance, validated_data):
        ranking = validated_data.get('ranking', instance.ranking)
        category = validated_data.get('category', instance.category)
        user = instance.user

        favorite_thing_id = instance.favorite_thing_id
        rankings_queryset = FavoriteThing.objects.order_by('ranking')\
            .filter(Q(category=category) & Q(user=user.user_id))

        if ranking > rankings_queryset.last().ranking + 1:
            ranking = rankings_queryset.last().ranking
            validated_data = {**validated_data, 'ranking': ranking}

        existing_ranking = rankings_queryset.filter(ranking=ranking)

        if existing_ranking and \
                existing_ranking.first().favorite_thing_id != \
                favorite_thing_id:
            if ranking > instance.ranking:
                next_rankings = rankings_queryset.filter(
                    ranking__range=(instance.ranking+1, ranking))
                reorder_rankings_subtract(next_rankings)
            else:
                next_rankings = rankings_queryset.filter(
                    ranking__range=(ranking, instance.ranking-1))
                reorder_rankings(next_rankings)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        try:
            instance.save()
            return instance
        except IntegrityError:
            raise serializers.ValidationError(
                'Favorite thing already exist in database')
