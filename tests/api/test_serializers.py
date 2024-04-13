import pytest
from rest_framework.test import APITestCase

from api.models import Book
from api.serializers import BookSerializer


@pytest.mark.django_db
class TestBookSerializer(APITestCase):
    fixtures = ["fixtures.json"]

    def test_book_serializer_visible_columns(self):
        book_instance = Book.objects.get(name="Karlsson-on-the-Roof")
        visible_columns = ["name", "author", "price"]
        serializer = BookSerializer(
            instance=book_instance, context={"visible_columns": visible_columns}
        )
        serialized_data = serializer.data
        assert len(visible_columns) + 1 == len(
            serialized_data
        )  # 'id' column exists always
        assert "name" in serialized_data
        assert "author" in serialized_data
        assert "price" in serialized_data
        assert "id" in serialized_data
        assert "description" not in serialized_data
