from rest_framework import serializers

from .models import Book, Profile


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "name", "title", "author", "description", "price"]

    def validate_price(self, price):
        if not (0 < price < 100_000):
            raise serializers.ValidationError(
                "Price must be more than 0 and less than 100 000"
            )
        return price

    def to_representation(self, instance):
        data = super().to_representation(instance)
        visible_columns = self.context.get("visible_columns", [])
        return {key: value for key, value in data.items() if key in visible_columns} | {
            "id": data["id"]
        }


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ["column_name", "is_visible"]
        extra_kwargs = {"url": {"lookup_field": "column_name"}}
