from dataclasses import dataclass
from task_queue_system.exceptions import TaskQueueException
import heapq


@dataclass
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int


@dataclass
class Task:
    priority: int
    id: int
    resources: Resources
    content: str
    result: str = ''

    def __post_init__(self):
        if self.priority <= 0:
            raise ValueError(f"Values for {self.priority} have to be positive!")
    # When using this Task in heapq, the priority will be negated to ensure
    # that higher numbers are treated as higher priority


class TaskQueue:
    def __init__(self):
        self._tasks = []
        self._index = 0

    def add_task(self, task: Task):
        if not isinstance(task, Task):
            raise TypeError("Only Task instances can be added.")
        # Negate the priority here
        heapq.heappush(self._tasks, (-task.priority, self._index, task))
        self._index += 1

    def get_task(self, available_resources: Resources) -> Task:
        if not self._tasks:
            raise TaskQueueException("No tasks in the queue.")

        temp_tasks = []
        res_task = None
        while self._tasks:
            _, index, task = heapq.heappop(self._tasks)
            if self._check_sufficiency_resources(task.resources, available_resources):
                res_task = task
                break
            else:
                temp_tasks.append((-task.priority, index, task))

        # Restore the other tasks to the heap
        for priority, index, task in temp_tasks:
            heapq.heappush(self._tasks, (priority, index, task))

        if res_task:
            return res_task
        # If no suitable task is found, raise exception
        raise TaskQueueException("No suitable task found for the given resources.")

    @staticmethod
    def _check_sufficiency_resources(required_resources: Resources, available_resources: Resources) -> bool:
        return (
                required_resources.ram <= available_resources.ram
                and required_resources.cpu_cores <= available_resources.cpu_cores
                and required_resources.gpu_count <= available_resources.gpu_count
        )
