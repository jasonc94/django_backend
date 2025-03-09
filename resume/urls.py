from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r"companies", CompanyViewSet)
router.register(r"projects", ProjectViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
