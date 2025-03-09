from rest_framework import serializers
from .models import Company, Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "start_date", "end_date", "description", "technologies"]


class CompanySerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(
        many=True, read_only=True
    )  # Nested serialization for projects

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "description",
            "logo_url",
            "projects",
        ]
