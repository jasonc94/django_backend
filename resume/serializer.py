from rest_framework import serializers
from .models import Company, Project


class ProjectSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Project
        fields = [
            "id",
            "company",
            "name",
            "start_date",
            "end_date",
            "description",
            "technologies",
        ]


class CompanySerializer(serializers.ModelSerializer):
    # serialize company projects
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "description",
            "logo",
            "projects",
        ]
