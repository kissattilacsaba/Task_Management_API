"""
Helpers for tasks_module
"""

import logging
import traceback
import numpy as np
from sentence_transformers import SentenceTransformer
from .models import Task, TaskSimilarity

logger = logging.getLogger('gunicorn.error')
model = SentenceTransformer('all-MiniLM-L6-v2')

def update_task_similarities():
    """
    Update task similarities based on their titles and descriptions
    """
    try:
        logger.info("Updating task similarities...")

        # Collect all tasks from the DB
        tasks = list(Task.objects.all())
        if len(tasks) == 0:
            return

        # Merge titles and descriptions, extract embeddings,
        titles = [task.title + ' ' + task.description for task in tasks]
        embeddings = model.encode(titles, convert_to_numpy=True)

        # Normalize embeddings and compute similarity matrix
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / norms
        similarity_matrix = np.dot(embeddings, embeddings.T)

        # For every task, find the top 5 most similar tasks
        similarity_entries = []
        for i, current_task in enumerate(tasks):
            row = similarity_matrix[i]
            sorted_idxs = np.argsort(-row)[1:6]
 
            for idx in sorted_idxs:
                similar_task = tasks[idx]
                score = row[idx]
                similarity_entries.append(
                    TaskSimilarity(
                        task=current_task,
                        similar=similar_task,
                        score=score
                    )
                )
        
        # Delete existing similarities and create new ones
        TaskSimilarity.objects.all().delete()
        TaskSimilarity.objects.bulk_create(similarity_entries)
        logger.info("Finished updating task similarities.")
    except Exception as error:
        logger.error(f"Error updating task similarities: {''.join(traceback.format_exception(error))}")