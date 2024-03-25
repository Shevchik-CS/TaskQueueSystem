# TaskQueueSystem

The TaskQueueSystem is a Python-based solution designed to manage and process tasks with varying priorities and resource requirements.
It enables efficient task scheduling by considering each task's priority and the resources it requires, ensuring that tasks are processed as resources become available.


## Restrictions
- This module implies that consumers often come with enough resources to complete tasks, otherwise the algorithm will not work efficiently.
- Task priorities must be positive.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pytest (for running tests)

### Installation

Clone this repository to your local machine:

```
git clone https://github.com/Shevchik-CS/TaskQueueSystem.git
cd TaskQueueSystem
```

### Running Tests

Ensure you have `pytest` installed. If not, install it using pip:

```
pip install pytest
```

To run the tests and verify the system, use the following command:

```
pytest tests
```
or

```
python -m pytest tests
```

## Usage

To use the TaskQueueSystem in your project, import the `TaskQueue`, `Task`, and `Resources` classes from the `task_queue_system` module:

```python
from task_queue_system import Task, Resources, TaskQueue

# Initialize the task queue
task_queue = TaskQueue()

# Create a task with resource requirements
task = Task(priority=1, id=123, resources=Resources(ram=4, cpu_cores=2, gpu_count=1), content="Example Task")

# Add the task to the queue
task_queue.add_task(task)

# Fetch and process a task, given available resources
available_resources = Resources(ram=8, cpu_cores=4, gpu_count=2)
task = task_queue.get_task(available_resources)
```