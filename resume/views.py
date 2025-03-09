from rest_framework import viewsets
from .models import Company, Project
from resume.serializer import CompanySerializer, ProjectSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
