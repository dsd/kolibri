import mock
from django.test.testcases import TestCase

from kolibri.core.tasks.job import Job
from kolibri.core.tasks.job import RegisteredJob


class JobTest(TestCase):
    def setUp(self):
        self.job = Job(id)
        self.job.storage = mock.MagicMock()

    def test_job_save_as_cancellable(self):
        cancellable = not self.job.cancellable

        self.job.save_as_cancellable(cancellable=cancellable)
        self.job.storage.save_job_as_cancellable.assert_called_once_with(
            self.job.job_id, cancellable=cancellable
        )

    def test_job_save_as_cancellable__skip(self):
        cancellable = self.job.cancellable
        self.job.save_as_cancellable(cancellable=cancellable)
        self.job.storage.save_job_as_cancellable.assert_not_called()

    def test_job_save_as_cancellable__no_storage(self):
        cancellable = not self.job.cancellable
        self.job.storage = None
        with self.assertRaises(ReferenceError):
            self.job.save_as_cancellable(cancellable=cancellable)


class TestRegisteredJob(TestCase):
    def setUp(self):
        self.registered_job = RegisteredJob(
            int,
            validator=int,
            priority="high",
            permission_classes=[int],
            job_id="test",
            group="human",
            cancellable=True,
            track_progress=True,
        )

    def test_constructor_sets_required_params(self):
        self.assertEqual(self.registered_job.func, int)
        self.assertEqual(self.registered_job.validator, int)
        self.assertEqual(self.registered_job.priority, "HIGH")
        self.assertEqual(self.registered_job.permissions, [p() for p in [int]])
        self.assertEqual(self.registered_job.job_id, "test")
        self.assertEqual(self.registered_job.group, "human")
        self.assertEqual(self.registered_job.cancellable, True)
        self.assertEqual(self.registered_job.track_progress, True)
        self.assertEqual(self.registered_job.extra_metadata, {})

    @mock.patch("kolibri.core.tasks.job.Job")
    def test__ready_job_initializes_job_and_clears_metadata(self, MockJob):
        self.registered_job = mock.MagicMock(extra_metadata={"meta": "test"})

        self.registered_job._ready_job("10", base=10)

        MockJob.assert_called_once_with(
            int,
            "10",  # arg that was passed to _ready_job()
            job_id="test",
            group="human",
            cancellable=True,
            track_progress=True,
            extra_metadata={"meta": "test"},
            base=10,  # kwarg that was passed to _ready_job()
        )

        # Do we clear metadata after creating job object?
        self.registered_job.extra_metadata.clear.assert_called_once()

    def test__ready_job_returns_job_object(self):
        result = self.registered_job._ready_job("10", base=10)
        self.assertIsInstance(result, Job)

    @mock.patch("kolibri.core.tasks.job.RegisteredJob._ready_job")
    @mock.patch("kolibri.core.tasks.main.scheduler")
    def test_enqueue_in(self, mock_scheduler, _ready_job_mock):
        args = ("10",)
        kwargs = dict(base=10)

        _ready_job_mock.return_value = "job"

        self.registered_job.enqueue_in(
            delta_time="delta_time",
            interval=10,
            repeat=10,
            args=args,
            kwargs=kwargs,
        )

        _ready_job_mock.assert_called_once_with(*args, **kwargs)
        mock_scheduler.enqueue_in.assert_called_once_with(
            func="job",
            delta_t="delta_time",
            interval=10,
            repeat=10,
        )

    @mock.patch("kolibri.core.tasks.job.RegisteredJob._ready_job")
    @mock.patch("kolibri.core.tasks.main.scheduler")
    def test_enqueue_at(self, mock_scheduler, _ready_job_mock):
        args = ("10",)
        kwargs = dict(base=10)

        _ready_job_mock.return_value = "job"

        self.registered_job.enqueue_at(
            datetime="datetime",
            interval=10,
            repeat=10,
            args=args,
            kwargs=kwargs,
        )

        _ready_job_mock.assert_called_once_with(*args, **kwargs)
        mock_scheduler.enqueue_at.assert_called_once_with(
            func="job",
            dt="datetime",
            interval=10,
            repeat=10,
        )

    @mock.patch("kolibri.core.tasks.job.RegisteredJob._ready_job")
    def test_enqueue(self, _ready_job_mock):
        mock_queue = mock.MagicMock()

        with mock.patch.dict(
            "kolibri.core.tasks.main.PRIORITY_TO_QUEUE_MAP",
            {"REGULAR": mock_queue, "HIGH": mock_queue},
        ):
            args = ("10",)
            kwargs = dict(base=10)

            _ready_job_mock.return_value = "job"

            self.registered_job.enqueue(*args, **kwargs)

            _ready_job_mock.assert_called_once_with(*args, **kwargs)
            mock_queue.enqueue.assert_called_once_with(func="job")
