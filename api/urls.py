from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, ProfileViewSet

app_name = "api"

router_v1 = DefaultRouter()

router_v1.register("books", BookViewSet)
router_v1.register("profiles", ProfileViewSet)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
