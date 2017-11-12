"""Server-like task scheduler and processor."""
import abc
import threading

import six

from jarvis.worker import base

RETRY_INTERVAL = 0.1


@six.add_metaclass(abc.ABCMeta)
class Executor(base.Worker):
    """Contract class for all the executors."""

    def __init__(self, delay, loop):
        """Instantiate a new executor."""
        super(Executor, self).__init__()
        self._queue = []
        self._delay = delay
        self._loop = loop
        self._stop_event = threading.Event()

    @abc.abstractmethod
    def on_task_done(self, task, result):
        """What to execute after successfully finished processing a task."""
        pass

    @abc.abstractmethod
    def on_task_fail(self, task, exc):
        """What to do when the program fails processing a task."""
        pass

    @abc.abstractmethod
    def on_interrupted(self):
        """What to execute when keyboard interrupts arrive."""
        pass

    def _get_task(self):
        """Retrieve a task from the queue."""
        if self._queue:
            return self._queue.pop()

    def _work(self, task):
        """Run the received task and process the result."""
        # pylint: disable=broad-except
        try:
            return task.run()
        except Exception as exc:
            self.on_task_fail(task, exc)

    def put_task(self, task):
        """Add a task to the tasks queue."""
        if not isinstance(task, base.Task):
            raise ValueError("Invalid type of task provided.")
        self._queue.append(task)

    def run(self):
        """Process incoming tasks."""
        self.prologue()
        while not self._stop_event.is_set():
            try:
                task = self._get_task()
                if task:
                    self._work(task)
                if not self._loop:
                    break
            except KeyboardInterrupt:
                self.on_interrupted()
                break
        self.epilogue()


@six.add_metaclass(abc.ABCMeta)
class ConcurrentExecutor(base.ConcurrentWorker):
    """Abstract base class for concurrent workers."""

    def __init__(self, delay, workers_count, queue_size):
        """Instantiate with custom number thread safe objects."""
        super(ConcurrentExecutor, self).__init__(delay=delay,
                                                 workers_count=workers_count)
        self._queue = six.moves.queue.Queue(queue_size)

    def _put_task(self, task):
        """Add a task to the queue."""
        self._queue.put(task)

    def _get_task(self):
        """Retrieve a task from the queue."""
        try:
            return self._queue.get(block=True, timeout=self._delay)
        except six.moves.queue.Empty:
            pass

    def _start_worker(self):
        """Create a custom worker and return its object."""
        print("Creating new worker.")

        def _worker(self):
            """Worker able to retrieve and process tasks."""
            print("Worker starting...")
            while not self._stop_event.is_set():
                task = self._get_task()
                if not task:
                    print("Nothing to do.")
                    continue
                task.run()

        worker = threading.Thread(target=_worker)
        worker.setDaemon(True)
        worker.start()
        return worker

    def on_task_done(self, task, result):
        """What to execute after successfully finished processing a task."""
        self._queue.task_done()
        print(task, result)

    def on_task_fail(self, task, exc):
        """What to do when the program fails processing a task."""
        print(task, exc)

    def on_interrupted(self):
        """Mark the processing as stopped."""
        self._stop_event.set()
        super(ConcurrentExecutor, self).on_interrupted()
