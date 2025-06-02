# Task Management RESTful API

This is a basic RESTful API that allows users to create, read, update and delete tasks.

## Setup instructions

Clone the repository and enter the directory
```
git clone https://github.com/kissattilacsaba/Task_Management_API.git
cd Task_Management_API
```
In your (preferably virtual) Python environment install the dependencies:
```
pip install -r requirements.txt
```
Create the database tables:
```
python manage.py migrate
```
Optionally seed the database:
```
python seed_tasks.py
```
Start the server:
```
gunicorn Task_Management_App.wsgi --config gunicorn_config.py
```

(A docker setup was also created, but it had problems with the BackgroundScheduler, so it was left out for now)
## API endpoint documentation

Following the above setup, the base url of the API is: `http://127.0.0.1:8000` The endpoint have to be appended to it.


One Task has the following fields:
* `id`: id of the task
* `title`: title of the task
* `description`: description of the task
* `creation_date`: creation date of the task in format 'YYYY-MM-DD'
* `due_date`: due date of the task in format 'YYYY-MM-DD'
* `status`: status of the task, can be `pending`, `in_progress`, `completed`, `overdue`, `cancelled`

### List all Tasks
Retrieve a list of all tasks

Endpoint: `GET /api/tasks/`

Query parameters:
* `status`: only Tasks with this status are returned
* `due_date`: only Tasks with this specific due_date are returned
* `due_date_before`: only Tasks with due_date before this are returned
* `due_date_after`: only Tasks with due_date after this are returned
* `ordering`: determines the order of the returned Tasks. Possible values:
    * `creation_date`: sorted by creation_date in ascending order
    * `-creation_date`: sorted by creation_date in descending order
    * `due_date`: sorted by due_date in ascending order
    * `-due_date`: sorted by due_date in descending order

Example request:

`GET /api/tasks?status=completed&ordering=-due_date`

Example response:

`200 OK`
```json
[
  {
    "id": 1,
    "title": "Write project proposal",
    "description": "Draft and submit the new project proposal by end of week.",
    "creation_date": "2025-06-01",
    "due_date": "2025-06-07",
    "status": "completed"
  },
  {
    "id": 2,
    "title": "Review financial report",
    "description": "",
    "creation_date": "2025-05-28",
    "due_date": "2025-06-03",
    "status": "completed"
  },
]
```
### Create a new Task
Creates a new Task. `title`, `creation_date`, `due_date` fields are required, `status` defaults to 'pending'.

Endpoint: `POST /api/tasks/`

Example request body:
```json
{
  "title": "A new task",
  "creation_date": "2025-06-01",
  "due_date": "2025-06-07"
}
```
Example response:

`201 Created`
```json
{
  "id": 12,
  "title": "A new task",
  "description": "",
  "creation_date": "2025-06-01",
  "due_date": "2025-06-07",
  "status": "pending"
}
```
### Retrieve a Task
Retrieve the Task with the given id

Path Parameter: `id` - id of the Task to be deleted

Endpoint: `GET /api/tasks/12/`

Example response:

`200 OK`
```json
{
  "id": 10,
  "title": "Pick up prescription",
  "description": "Visit the pharmacy before it closes.",
  "creation_date": "2025-05-30",
  "due_date": "2025-06-01",
  "status": "cancelled"
}
```

### Update a Task
Replace all fields of the Task with the given id. `title`, `creation_date`, `due_date` fields are required to be sent.

Path Parameter: `id` - id of the Task to be deleted

Endpoint: `PUT /api/tasks/12/`

Example request body:
```json
{
  "title": "Changed title",
  "creation_date": "2025-06-01",
  "due_date": "2025-06-07",
  "status": "in_progress"
}
```
Example response:

`200 OK`
```json
{
  "id": 12,
  "title": "Changed title",
  "description": "",
  "creation_date": "2025-06-01",
  "due_date": "2025-06-07",
  "status": "in_progress"
}
```

### Partially update a Task
Modify one or more fields of the Task with the given id. Only the fields included in the request body will be updated.

Path Parameter: `id` - id of the Task to be deleted

Endpoint: `PATCH /api/tasks/12/`

Example request body:
```json
{
  "due_date": "2025-06-10",
  "status": "completed"
}
```
Example response:

`200 OK`
```json
{
  "id": 12,
  "title": "Changed title",
  "description": "",
  "creation_date": "2025-06-01",
  "due_date": "2025-06-10",
  "status": "completed"
}
```

### Delete a Task
Delete the Task with the given id from the database.

Path Parameter: `id` - id of the Task to be deleted

Endpoint: 
`DELETE /api/tasks/13/`

Example response:
`204 No Contet`

### Smart Task Suggestions
Suggest actions for Tasks based on pevious actions. The software currently only monitors Task status changes and suggests changing the status of similar Tasks.

In the response one suggestion has the next fields:
* `task_id`: id of the task that should be modified
* `task`: title of the task that should be modified
* `new_satus`: the new suggested status of the task 

Endpoint: 
`GET /api/tasks/suggestions/`

Example response:

`200 OK`
```json
[
  {
    "task_id": 8,
    "task": "Clean the bathroom",
    "new_status": "completed"
  },
  {
    "task_id": 4,
    "task": "Call the plumber",
    "new_status": "in_progress"
  },
]
```

## Design decisions

* As it was not mentioned in the task description, no authentication or authorization mechanism is implemented. In a real application there should be a way to authenticate and the Tasks of the different users should be handled separately.
* Testing was not implemented as it was deemed excessive for the scope of the app
* Django REST framework was used to create basic CRUD functionality as it provides this out-of-the-box

### Smart task suggestion approach

The current smart task suggestion feature fetches the most recently modified Tasks, finds the  Tasks with the most similar name and "suggests" the modification of their statuses.

For this to work, every time the status of a Task is modified, this modification with the new status is stored in DB.

A periodic background task takes the `title` and the `description` of every stored Task and creates an embedding vector from them using a Machine Learning model. This way for every Task the cosine similarity with every other Task is computed and the IDs of the most similar Tasks are saved in the DB. Right now this periodic task is executed every minute, to ensure the similarities are present during testing. In a real application the task would run every hour or day. The task could also be further optimized as its complexity now is O(n^2) and with many more Tasks this could case problems.

When the `GET /api/tasks/suggestions/` endpoint is called, it finds the most recent status changes and based on the stored similarities, the most similar tasks are found for every changed task. Then "suggestions" are created, meaning that the similar tasks are paired with the new status of the recently chaged tasks, and these "suggestion" are returned.

The exact settings should be fine-tuned based on the intended use and the number of Tasks.

Further improvement ideas: 

Not only the status changes, but other changes of a Task and their creation, deletion is also stored in the DB. Then this information is used in some way to create suggestions.

With Data Science methods the Tasks could be grouped based on their attributes and new suggestions could be generated based on these groups.

Finally, some LLM model could be integrated that receives the modification history of the Tasks and it generates suggestions.

It was found that implementing the above ideas is out of scope for this inerview task, so the more basic approach was implemented