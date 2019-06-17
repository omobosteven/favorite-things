from rest_framework import serializers
from core.models import Category, CategoryUser


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Category
        fields = (
            'category_id', 'name', 'default', 'user'
        )
        read_only_fields = ('user',)

    def create(self, validated_data):
        user = validated_data.get('user')
        validated_data.pop('user')
        if user.is_superuser:
            validated_data.update({'default': True})
        category = Category.objects.create(**validated_data)
        CategoryUser.objects.create(user=user, category=category)

        return category
