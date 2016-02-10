"""Server-like task scheduler and processor."""
import abc
import time
import threading

import six

from jarvis.common import exception


@six.add_metaclass(abc.ABCMeta)
class Worker(object):

    """Contract class for all the commands and clients."""

    def __init__(self):
        self._name = self.__class__.__name__

    @property
    def name(self):
        """The name of the current worker."""
        return self._name

    def prologue(self):
        """Executed once before the command running."""
        pass

    @abc.abstractmethod
    def on_interrupted(self):
        """What to execute when keyboard interrupts arrive."""
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
        self.prologue()
        result = self.work()
        self.epilogue()

        return result


@six.add_metaclass(abc.ABCMeta)
class ConcurrentWorker(Worker):

    """Contract class for all the concurrent workers."""

    def __init__(self, delay, workers_count):
        super(ConcurrentWorker, self).__init__()
        self._delay = delay
        self._workers_count = workers_count     # desired number of workers
        self._workers = []                      # workers as objects
        self._manager = None                    # who supervises the workers
        self._stop_event = threading.Event()

    @abc.abstractmethod
    def _put_task(self, task):
        """Adds a task to the queue."""
        pass

    @abc.abstractmethod
    def _get_task(self):
        """Retrieves a task from the queue."""
        pass

    @abc.abstractmethod
    def _task_generator(self):
        """Override this with your custom task generator."""
        pass

    @abc.abstractmethod
    def _start_worker(self):
        """Create a custom worker and return its object."""
        pass

    def _manage_workers(self):
        """Maintain a desired number of workers up."""
        while not self._stop_event.is_set():
            # Check if all the workers are alive
            for worker in self._workers[:]:
                if not worker.is_alive():
                    self._workers.remove(worker)

            # Check if all the workers are running
            if len(self._workers) == self._workers_count:
                time.sleep(self._delay)
                continue

            # Create a new worker
            worker = self._start_worker()
            self._workers.append(worker)

    def prologue(self):
        """Start a parallel supervisor."""
        super(ConcurrentWorker, self).prologue()
        self._manager = threading.Thread(target=self._manage_workers)
        self._manager.start()

    def run(self):
        """Starts a series of workers and processes incoming tasks."""
        self.prologue()
        try:
            while not self._stop_event.is_set():
                # Adding task in the processing queue
                for task in self._task_generator():
                    self._put_task(task)
                time.sleep(self._delay)
        except KeyboardInterrupt:
            self.on_interrupted()
        self.epilogue()

    def epilogue(self):
        """Wait for that supervisor and its workers."""
        self._manager.join()
        for worker in self._workers:
            if worker.is_alive():
                worker.join()

        super(ConcurrentWorker, self).epilogue()


@six.add_metaclass(abc.ABCMeta)
class Task(Worker):

    """Contract class for all the tasks."""

    def __init__(self, executor=None):
        super(Task, self).__init__()
        self._executor = executor

    def task_done(self, result):
        """What to execute after successfully finished processing a task."""
        callback = getattr(self._executor, "on_task_done")
        if callback:
            callback(self, result)

    def task_fail(self, exc):
        """What to do when the program fails processing a task."""
        callback = getattr(self._executor, "on_task_fail")
        if callback:
            callback(self, exc)

    @abc.abstractmethod
    def work(self):
        """Override this with your desired procedures."""
        pass

    def run(self):
        """Run the command."""
        result = None

        self.prologue()
        try:
            result = self.work()
        except exception.JarvisException as exc:
            self.task_fail(exc)
        except KeyboardInterrupt:
            self.on_interrupted()
        else:
            self.task_done(result)
        self.epilogue()

        return result
