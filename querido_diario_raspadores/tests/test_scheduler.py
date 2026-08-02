from unittest.mock import Mock

from scrapinghub.hubstorage.serialization import MSGPACK_AVAILABLE

import scheduler


def test_messagepack_is_available():
    assert MSGPACK_AVAILABLE


def test_schedule_job_reuses_provided_project(monkeypatch):
    project = Mock()
    job_settings = {"FILES_STORE": "test"}
    monkeypatch.setattr(scheduler, "_job_settings", Mock(return_value=job_settings))
    monkeypatch.setattr(
        scheduler,
        "_get_project",
        Mock(side_effect=AssertionError("A new project client was created")),
    )

    scheduler._schedule_job(
        start="2026-08-01",
        full=False,
        spider_name="test_spider",
        project=project,
    )

    project.spiders.get.assert_called_once_with("test_spider")
    project.spiders.get.return_value.jobs.run.assert_called_once_with(
        job_settings=job_settings,
        job_args={"start": "2026-08-01"},
    )


def test_schedule_enabled_spiders_creates_project_once(monkeypatch):
    project = Mock()
    get_project = Mock(return_value=project)
    schedule_job = Mock()
    monkeypatch.setattr(scheduler, "_get_project", get_project)
    monkeypatch.setattr(
        scheduler,
        "_get_enabled_spiders",
        Mock(return_value=["first_spider", "second_spider"]),
    )
    monkeypatch.setattr(scheduler, "_schedule_job", schedule_job)

    scheduler.schedule_enabled_spiders.callback()

    get_project.assert_called_once_with()
    assert schedule_job.call_count == 2
    assert all(
        call.kwargs["project"] is project for call in schedule_job.call_args_list
    )
