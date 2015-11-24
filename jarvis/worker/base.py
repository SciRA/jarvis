"""Server-like task scheduler and processor."""
import abc
import time
import threading

import six

from jarvis import config as global_config


@six.add_metaclass(abc.ABCMeta)
class Worker(object):

    """Abstract base class for simple workers."""

    def __init__(self, name, delay=global_config["misc.retry_interval"],
                 loop=True):
        """Setup a new instance."""
        self._name = name
        self._delay = delay
        self._loop = loop

    def prologue(self):
        """Executed once before the main procedures."""
        pass

    def epilogue(self):
        """Executed once after the main procedures."""
        pass

    @abc.abstractmethod
    def task_generator(self):
        """Override this with your custom task generator."""
        pass

    @abc.abstractmethod
    def process(self, task):
        """Override this with your desired procedures."""
        pass

    def _process(self, task):
        """Wrapper over the `process`."""
        # pylint: disable=W0703
        try:
            result = self.process(task)
        except Exception as exc:
            self.task_fail(task, exc)
        else:
            self.task_done(task, result)

    def put_task(self, task):
        """Adds the task in the queue."""
        self._process(task)

    def task_done(self, task, result):
        """What to execute after successfully finished processing a task."""
        pass

    def task_fail(self, task, exc):
        """What to do when the program fails processing a task."""
        pass

    def finished(self):
        """What to execute after finishing processing all the tasks."""
        return self._loop    # decide to continue reprocessing or not

    def interrupted(self):
        """What to execute when keyboard interrupts arrive."""
        pass

    def start(self):
        """Starts a series of workers and processes incoming tasks."""
        self.prologue()
        while True:
            try:
                for task in self.task_generator():
                    self.put_task(task)
                loop = self.finished()
                if not loop:
                    break
                time.sleep(self._delay)
            except KeyboardInterrupt:
                self.interrupted()
                break
        self.epilogue()


class ConcurrentWorker(Worker):

    """Abstract base class for concurrent workers."""

    def __init__(self, queue_size, workers_count, *args, **kwargs):
        """Instantiates with custom number thread safe objects."""
        super(ConcurrentWorker, self).__init__(*args, **kwargs)
        self._workers_count = workers_count     # desired number of workers
        self._workers = []                      # workers as objects
        self._manager = None                    # who supervises the workers
        self._queue = six.moves.queue.Queue(queue_size)  # processing queue
        # event telling that all the things must end
        self._stop = threading.Event()

    def start_worker(self):
        """Create a custom worker and return its object."""
        worker = threading.Thread(target=self.work)
        worker.setDaemon(True)
        worker.start()
        return worker

    def manage_workers(self):
        """Maintain a desired number of workers up."""
        while not self._stop.is_set():
            for worker in self._workers[:]:
                if not worker.is_alive():
                    self._workers.remove(worker)

            if len(self._workers) == self._workers_count:
                time.sleep(global_config["misc"].retry_interval)
                continue

            worker = self.start_worker()
            self._workers.append(worker)

    def prologue(self):
        """Start a parallel supervisor."""
        super(ConcurrentWorker, self).prologue()
        self._manager = threading.Thread(target=self.manage_workers)
        self._manager.start()

    def epilogue(self):
        """Wait for that supervisor and its workers."""
        self._manager.join()
        self._queue.join()
        for worker in self._workers:
            if worker.is_alive():
                worker.join()

        super(ConcurrentWorker, self).epilogue()

    def interrupted(self):
        """Mark the processing as stopped."""
        self._stop.set()
        super(ConcurrentWorker, self).interrupted()

    def put_task(self, task):
        """Adds a task to the queue."""
        self._queue.put(task)

    def get_task(self):
        """Retrieves a task from the queue."""
        return self._queue.get()

    def task_done(self, task, result):
        self._queue.task_done()
        super(ConcurrentWorker, self).task_done(task, result)

    def work(self):
        """Worker able to retrieve and process tasks."""
        while not self._stop.is_set():
            task = self.get_task()
            self._process(task)
