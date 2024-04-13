import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Book, Profile


@pytest.mark.django_db
class TestProfileViewSet(APITestCase):
    fixtures = ["fixtures.json"]

    def test_list_visible_profiles(self):
        assert Profile.objects.count() == 5
        response = self.client.get(reverse("api:profile-list"))
        assert response.status_code == status.HTTP_200_OK
        visible_profiles = Profile.objects.filter(is_visible=True)
        assert response.data["count"] == visible_profiles.count()

    def test_create_profile_not_allowed(self):
        profiles_count_before = Profile.objects.count()
        url = reverse("api:profile-list")
        new_profile = {"column_name": "new_profile"}
        response = self.client.post(url, new_profile, format="json")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert Profile.objects.count() == profiles_count_before

    def test_update_column_name_not_allowed(self):
        profile_name_instance = Profile.objects.get(column_name="name")
        url = reverse("api:profile-detail", args=[profile_name_instance.column_name])
        new_data = {"column_name": "new_name"}
        response = self.client.patch(url, new_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        updated_profile = Profile.objects.get(pk=profile_name_instance.pk)
        assert updated_profile.column_name == profile_name_instance.column_name

    def test_update_visibility_allowed(self):
        visible_profiles_before = Profile.objects.filter(is_visible=True).count()
        profile_name_instance = Profile.objects.get(column_name="name")
        url = reverse("api:profile-detail", args=[profile_name_instance.column_name])
        new_data = {"is_visible": False}
        response = self.client.patch(url, new_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        visible_profiles_after = Profile.objects.filter(is_visible=True)
        assert visible_profiles_before == visible_profiles_after.count() + 1

        new_data = {"is_visible": True}
        response = self.client.patch(url, new_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        visible_profiles_after = Profile.objects.filter(is_visible=True)
        assert visible_profiles_before == visible_profiles_after.count()

    def test_delete_profile_not_allowed(self):
        profiles_count_before = Profile.objects.count()
        profile_name_instance = Profile.objects.get(column_name="name")
        url = reverse("api:profile-detail", args=[profile_name_instance.column_name])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert Profile.objects.count() == profiles_count_before


@pytest.mark.django_db
class TestBookViewSet(APITestCase):
    fixtures = ["fixtures.json"]

    def test_list_books(self):
        assert Book.objects.count() == 16
        response = self.client.get(reverse("api:book-list"))
        assert response.status_code == status.HTTP_200_OK
        assert "name" in response.data["results"][0]

        profile_name_instance = Profile.objects.get(column_name="name")
        url = reverse("api:profile-detail", args=[profile_name_instance.column_name])
        new_data = {"is_visible": False}
        response = self.client.patch(url, new_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        response = self.client.get(reverse("api:book-list"))
        assert response.status_code == status.HTTP_200_OK
        assert "name" not in response.data["results"][0]

    def test_create_book_allowed(self):
        books_count_before = Book.objects.count()
        url = reverse("api:book-list")
        new_book = {
            "name": "new_name",
            "title": "new_title",
            "author": "new_author",
            "description": "new_description",
            "price": 42,
        }
        response = self.client.post(url, new_book, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.count() == books_count_before + 1

    def test_update_book_allowed(self):
        book_instance = Book.objects.get(name="Karlsson-on-the-Roof")
        url = reverse("api:book-detail", args=[book_instance.pk])
        new_data = {"description": "new_description"}
        response = self.client.patch(url, new_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        updated_book = Book.objects.get(pk=book_instance.pk)
        assert updated_book.description == new_data["description"]

    def test_delete_book_allowed(self):
        books_count_before = Book.objects.count()
        book_instance = Book.objects.get(name="Karlsson-on-the-Roof")
        url = reverse("api:book-detail", args=[book_instance.pk])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Book.objects.count() == books_count_before - 1
