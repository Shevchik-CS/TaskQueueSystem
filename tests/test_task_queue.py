# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
"""
Tests for TaskQueueSystem
"""
import pytest
from task_queue_system import Task, Resources, TaskQueue, TaskQueueException


def test_empty_queue_exception():
    tq = TaskQueue()
    with pytest.raises(TaskQueueException):
        tq.get_task(Resources(ram=8, cpu_cores=4, gpu_count=1))


def test_negative_priority_exception():
    tq = TaskQueue()
    with pytest.raises(ValueError):
        tq.add_task(Task(0, 1, Resources(ram=16, cpu_cores=8, gpu_count=2), "Bad Task"))


def test_no_suitable_task_exception():
    tq = TaskQueue()
    tq.add_task(Task(1, 100, Resources(ram=16, cpu_cores=8, gpu_count=2), "Expensive Task"))
    with pytest.raises(TaskQueueException):
        tq.get_task(Resources(ram=8, cpu_cores=4, gpu_count=1))


def test_add_and_retrieve_task():
    tq = TaskQueue()
    task = Task(1, 101, Resources(ram=4, cpu_cores=2, gpu_count=1), "Cheap Task")
    tq.add_task(task)
    retrieved_task = tq.get_task(Resources(ram=8, cpu_cores=4, gpu_count=1))
    assert task.id == retrieved_task.id


def test_add_and_retrieve_task_in_priority_order():
    tq = TaskQueue()
    task1 = Task(10, 101, Resources(ram=4, cpu_cores=2, gpu_count=1), "Cheap Task")
    task2 = Task(20, 100, Resources(ram=16, cpu_cores=8, gpu_count=2), "Expensive Task")
    task3 = Task(30, 102, Resources(ram=8, cpu_cores=4, gpu_count=1), "Normal Task")
    tq.add_task(task1)
    tq.add_task(task2)
    tq.add_task(task3)
    retrieved_task = tq.get_task(Resources(ram=20, cpu_cores=16, gpu_count=3))
    assert task3.id == retrieved_task.id


def test_large_scale():
    tq = TaskQueue()
    for i in range(2000):
        tq.add_task(Task(priority=1 + i % 100, id=i,
                         resources=Resources(ram=1 + i % 10, cpu_cores=1, gpu_count=1),
                         content=f"Task number {i}"))

    available_resources = Resources(ram=3, cpu_cores=2, gpu_count=1)
    fetched_tasks = 0
    try:
        while True:
            tq.get_task(available_resources)
            fetched_tasks += 1
    except TaskQueueException:
        pass

    assert fetched_tasks > 0, "Should fetch at least one task with sufficient resources."
