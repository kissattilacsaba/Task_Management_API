"""
Routes for the tasks_module
"""

from django.urls import path, include
from rest_framework import routers
from .views import TaskViewSet, smart_suggestions

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('tasks/suggestions', smart_suggestions),
    path('', include(router.urls)),
]