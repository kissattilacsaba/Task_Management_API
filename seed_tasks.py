import os
import django
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Task_Management_App.settings")
django.setup()

from tasks_module.models import *

def run():
    example_data = [
        {
            "title": "Buy groceries",
            "description": "Pick up milk, eggs, bread, and vegetables for the week.",
            "creation_date": datetime.date(2025, 5, 28),
            "due_date": datetime.date(2025, 6, 1),
            "status": "completed",
        },
        {
            "title": "Walk the dog",
            "description": "Evening walk around the neighborhood park.",
            "creation_date": datetime.date(2025, 5, 30),
            "due_date": datetime.date(2025, 6, 1),
            "status": "completed",
        },
        {
            "title": "Do laundry",
            "description": "Wash and fold clothes; separate colors and whites.",
            "creation_date": datetime.date(2025, 5, 31),
            "due_date": datetime.date(2025, 6, 2),
            "status": "in_progress",
        },
        {
            "title": "Call the plumber",
            "description": "Schedule repair for the leaking kitchen sink.",
            "creation_date": datetime.date(2025, 5, 29),
            "due_date": datetime.date(2025, 6, 3),
            "status": "pending",
        },
        {
            "title": "Pay utility bills",
            "description": "Electricity and water bills are due this week.",
            "creation_date": datetime.date(2025, 5, 27),
            "due_date": datetime.date(2025, 6, 1),
            "status": "completed",
        },
        {
            "title": "Water the plants",
            "description": "Indoor and balcony plants need watering twice this week.",
            "creation_date": datetime.date(2025, 5, 30),
            "due_date": datetime.date(2025, 6, 4),
            "status": "pending",
        },
        {
            "title": "Schedule dentist appointment",
            "description": "Call the clinic to book a check‐up for next month.",
            "creation_date": datetime.date(2025, 5, 25),
            "due_date": datetime.date(2025, 6, 5),
            "status": "overdue",
        },
        {
            "title": "Clean the bathroom",
            "description": "Scrub tub, sink, and toilet; mop the floor.",
            "creation_date": datetime.date(2025, 5, 31),
            "due_date": datetime.date(2025, 6, 2),
            "status": "in_progress",
        },
        {
            "title": "Prepare lunch for tomorrow",
            "description": "Cook pasta salad and portion into containers.",
            "creation_date": datetime.date(2025, 6, 1),
            "due_date": datetime.date(2025, 6, 1),
            "status": "pending",
        },
        {
            "title": "Pick up prescription",
            "description": "Visit the pharmacy before it closes.",
            "creation_date": datetime.date(2025, 5, 30),
            "due_date": datetime.date(2025, 6, 1),
            "status": "cancelled",
        },
    ]

    # Task.objects.all().delete()
    if Task.objects.count() > 0:
        print("Task table already contains data. Skipping seeding.")
        return
    
    for data in example_data:
        Task.objects.create(**data)

    print("Seeded Task table with example data.")

if __name__ == "__main__":
    run()
