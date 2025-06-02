"""
Serializers for the models in the tasks_module
"""

from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the Task model"""
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'creation_date',
            'due_date',
            'status',
        ]
        read_only_fields = ['id']