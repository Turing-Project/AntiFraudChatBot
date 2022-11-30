"""
async helpers
"""
from __future__ import annotations
import asyncio
from asyncio import Task
from typing import (
    List,
    Any,
    Optional,
    Set,
    TYPE_CHECKING
)
import functools

if TYPE_CHECKING:
    from wechaty import Message, WechatyPlugin


async def gather_with_concurrency(n_task: int, tasks: List[Task]) -> Any:
    """
    gather tasks with the specific number concurrency
    Args:
        n_task: the number of tasks
        tasks: task objects
    """
    semaphore = asyncio.Semaphore(n_task)

    async def sem_task(task: Task) -> Any:
        async with semaphore:
            return await task
    return await asyncio.gather(*(sem_task(task) for task in tasks))


class SingleIdContainer:
    """Store the Message Id Container"""
    _instance: Optional[SingleIdContainer] = None

    def __init__(self) -> None:
        self.ids: Set[str] = set()
        self.max_size: int = 100000

    def exist(self, message_id: str) -> bool:
        """exist if the message has been emitted

        Args:
            message_id (str): the identifier of message

        Returns:
            bool: if the message is the first message
        """
        if message_id in self.ids:
            return True
        self.ids.add(message_id)
        return False
    
    @classmethod
    def instance(cls) -> SingleIdContainer:
        """singleton pattern for MessageIdContainer"""
        if cls._instance is None or len(cls._instance.ids) > cls._instance.max_size:
            cls._instance = SingleIdContainer()

        return cls._instance


def single_message(on_message_func):    # type: ignore
    """single message decorator"""
    @functools.wraps(on_message_func)
    async def wrapper(plugin: WechatyPlugin, message: Message) -> None:
        if not SingleIdContainer.instance().exist(message.message_id):
            await on_message_func(plugin, message)
    return wrapper
