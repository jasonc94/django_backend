from django.db import models


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    logo = models.TextField(blank=True, null=True)


class Project(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="projects"
    )
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    technologies = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name
