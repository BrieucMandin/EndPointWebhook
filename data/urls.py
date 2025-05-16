from django.urls import path
from .views.views_webhook import webhook_receiver

urlpatterns = [
    path("", webhook_receiver, name="webhook_receiver"),
]
