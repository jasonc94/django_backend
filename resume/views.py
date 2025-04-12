from rest_framework import viewsets
from .models import Company, Project
from resume.serializer import CompanySerializer, ProjectSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Company.objects.order_by("-startDate")
    serializer_class = CompanySerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
