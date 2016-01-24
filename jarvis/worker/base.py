"""Server-like task scheduler and processor."""
import abc
import time
import threading

import six


@six.add_metaclass(abc.ABCMeta)
class Worker(object):

    """Contract class for all the commands and clients."""

    def __init__(self):
        self._name = self.__class__.__name__
        self._stop_event = threading.Event()

    @property
    def name(self):
        """The name of the current worker."""
        return self._name

    @property
    def stop(self):
        """Event used across the worker in order to treat the
        end of the execution for this worker.
        """
        return self._stop_event

    @abc.abstractmethod
    def task_done(self, result):
        """What to execute after successfully finished processing a task."""
        pass

    @abc.abstractmethod
    def task_fail(self, exc):
        """What to do when the program fails processing a task."""
        pass

    @abc.abstractmethod
    def interrupted(self):
        """What to execute when keyboard interrupts arrive."""
        pass

    def prologue(self):
        """Executed once before the command running."""
        pass

    @abc.abstractmethod
    def work(self):
        """Override this with your desired procedures."""
        pass

    def epilogue(self):
        """Executed once after the command running."""
        pass

    def run(self):
        """Run the command."""
        result = None

        try:
            self.prologue()
            result = self.work()
            self.epilogue()
        except KeyboardInterrupt:
            self.interrupted()
        except exception.JarvisException as exc:
            self.task_fail(exc)
        else:
            self.task_done(result)

        return result


@six.add_metaclass(abc.ABCMeta)
class Executor(object):

    """Contract class for all the executors."""

    def __init__(self, delay, loop):
        self._queue = []
        self._delay = delay
        self._loop = loop
        self._stop = threading.Event()

    @abc.abstractmethod
    def on_task_done(self, task, result):
        """What to execute after successfully finished processing a task."""
        pass

    @abc.abstractmethod
    def on_task_fail(self, task, exc):
        """What to do when the program fails processing a task."""
        pass

    @abc.abstractmethod
    def interrupted(self):
        """What to execute when keyboard interrupts arrive."""
        pass

    def prologue(self):
        """Executed once before the command running."""
        pass

    def epilogue(self):
        """Executed once after the command running."""
        pass

    def _get_task(self):
        """Retrieves a task from the queue."""
        if self._queue:
            return self._queue.pop()

    def _work(self, task):
        """Run the received task and process the result."""
        try:
            result = task.run()
        except Exception as exc:
            self.on_task_fail(task, exc)
        else:
            self.on_task_done(task, result)

    def put_task(self, task):
        """Adds a task to the tasks queue."""
        if not isinstance(task, Worker):
            raise ValueError("Invalid type of task provided.")
        self._queue.append(task)

    def run(self):
        """Processes incoming tasks."""
        self.prologue()
        while not self._stop_event.is_set():
            try:
                task = self._get_task()
                if task:
                    self._work(task)
                if not self._loop:
                    break
            except KeyboardInterrupt:
                self.interrupted()
                break
        self.epilogue()
