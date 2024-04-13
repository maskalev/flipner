from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Book, Profile
from .serializers import BookSerializer, ProfileSerializer


class BookViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows books to be created, viewed, edited and removed.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        visible_columns = Profile.objects.filter(is_visible=True).values_list(
            "column_name", flat=True
        )
        serializer = self.serializer_class(
            data=request.data, context={"visible_columns": visible_columns}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request):
        visible_columns = Profile.objects.filter(is_visible=True).values_list(
            "column_name", flat=True
        )
        books = self.get_queryset()

        page = self.paginate_queryset(books)
        if page is not None:
            serializer = self.serializer_class(
                page, many=True, context={"visible_columns": visible_columns}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(
            books, many=True, context={"visible_columns": visible_columns}
        )
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.method != "PATCH":
            raise MethodNotAllowed("PUT")
        visible_columns = Profile.objects.filter(is_visible=True).values_list(
            "column_name", flat=True
        )
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            context={"visible_columns": visible_columns},
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class ProfileViewSet(
    mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """
    API endpoint that allows profiles to be viewed or edited.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "column_name"

    def get_is_visible_queryset(self):
        return self.queryset.filter(is_visible=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_is_visible_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def test_delete_profile_not_allowed(self):
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
