from abc import ABC, abstractmethod
from uuid import UUID

from producer.src.domain.entities.task import Task


class TaskRepository(ABC):

    @abstractmethod
    async def create(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def get(self, task_id: UUID) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def update(self, task_id: UUID, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, task_id: UUID):
        raise NotImplementedError
