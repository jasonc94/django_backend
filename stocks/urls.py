from django.urls import path

from . import views

urlpatterns = [
    path("transactions/", views.TransactionListCreate.as_view(), name="transactions"),
]
