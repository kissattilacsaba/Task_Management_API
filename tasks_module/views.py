"""
Views for the tasks_module
""" 

import logging

from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.http import JsonResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, filters as drf_filters

from .models import Task, StatusHistory, TaskSimilarity
from .serializers import TaskSerializer

logger = logging.getLogger('gunicorn.error')


class TaskFilter(filters.FilterSet):
    """
    FilterSet for filtering tasks based on status and due date
    """

    status = filters.CharFilter(field_name='status', lookup_expr='exact')
    due_date = filters.DateFilter(field_name='due_date', lookup_expr='exact')
    due_date_before = filters.DateFilter(field_name='due_date', lookup_expr='lt')
    due_date_after  = filters.DateFilter(field_name='due_date', lookup_expr='gt')

    class Meta:
        model = Task
        fields = [
            'status',
            'due_date',
            'due_date_before',
            'due_date_after',
        ]

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, creating, updating, and deleting Tasks.
    """
    queryset = Task.objects.all().order_by('-creation_date')
    serializer_class = TaskSerializer

    filter_backends = [
        filters.DjangoFilterBackend,
        drf_filters.OrderingFilter,
    ]
    filterset_class = TaskFilter
    ordering_fields = [
        'creation_date',
        'due_date',
    ]
    ordering = ['creation_date']
    
    def perform_update(self, serializer: TaskSerializer):
        """
        Override the perform_update method to update status history
        """
        # Get current status
        task_instance = get_object_or_404(Task, pk=self.get_object().pk)
        old_status = task_instance.status

        # Perform default behavior
        updated_task = serializer.save()

        # Create a new StatusHistory entry if the status changed
        new_status = updated_task.status
        if old_status != new_status:
            StatusHistory.objects.create(
                task=updated_task,
                old_status=old_status,
                new_status=new_status
            )

@require_GET
def smart_suggestions(request: HttpRequest):
    """
    Provides smart suggestions based on recent task status changes
    """

    # Get the most recent status changes
    recent_changes = StatusHistory.objects.select_related('task').order_by('-timestamp')[:5]

    ## For every changed task find the most similar tasks and suggest to change their status
    suggesstions = set()
    for change in recent_changes:
        most_similars = TaskSimilarity.objects.filter(task=change.task).order_by('-score')[:2]
        for most_similar in most_similars:
            suggesstions.add((most_similar.similar.id,
                              most_similar.similar.title,
                              change.new_status))
            
    # Convert the set to a list of dictionaries
    suggesstions = [{
        'task_id': task_id,
        'task': task_title,
        'new_status': new_status
        } for task_id, task_title, new_status in suggesstions]
    
    return JsonResponse(suggesstions, safe=False)
