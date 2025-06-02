"""
Models used in the tasks_module
"""

from django.db import models

class Task(models.Model):
    """
    Model representing a task
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creation_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ], default='pending')

    # Many-to-many relationship with other tasks for similarity
    similar_tasks = models.ManyToManyField(
        'self',
        through='TaskSimilarity',
        symmetrical=False,
        related_name='similar_to',
    )

    def __str__(self):
        return self.title
    
class StatusHistory(models.Model):
    """
    Model representing a status change for a task
    """

    task = models.ForeignKey(Task, related_name='history', on_delete=models.CASCADE)
    old_status = models.CharField(max_length=20, choices=Task._meta.get_field('status').choices)
    new_status = models.CharField(max_length=20, choices=Task._meta.get_field('status').choices)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class TaskSimilarity(models.Model):
    """
    Model representing similarity between tasks
    """

    task       = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='similarity_origins')
    similar    = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='similarity_targets')
    
    score      = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('task', 'similar'),  # ensure no duplicate (task → similar) pairs
        ]