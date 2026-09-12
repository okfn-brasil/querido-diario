from unittest.mock import Mock

import click
import pytest
import requests
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


def test_enable_spider_uses_api_client(monkeypatch):
    api_client = Mock()
    monkeypatch.setattr(scheduler, "_get_api_client", Mock(return_value=api_client))

    scheduler.enable_spider.callback(spider_name="test_spider")

    api_client.set_spider_enabled.assert_called_once_with("test_spider", True)


def test_disable_spider_uses_api_client(monkeypatch):
    api_client = Mock()
    monkeypatch.setattr(scheduler, "_get_api_client", Mock(return_value=api_client))

    scheduler.disable_spider.callback(spider_name="test_spider")

    api_client.set_spider_enabled.assert_called_once_with("test_spider", False)


def test_job_settings_do_not_include_database_url(monkeypatch):
    monkeypatch.setenv("FILES_STORE", "test")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test")
    monkeypatch.setenv("AWS_ENDPOINT_URL", "test")
    monkeypatch.setenv("AWS_REGION_NAME", "test")
    monkeypatch.setenv("SPIDERMON_DISCORD_FAKE", "True")
    monkeypatch.setenv("SPIDERMON_DISCORD_WEBHOOK_URL", "test")
    monkeypatch.setenv("ZYTE_SMARTPROXY_APIKEY", "test")

    job_settings = scheduler._job_settings()

    assert "QUERIDODIARIO_DATABASE_URL" not in job_settings


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


def test_schedule_job_retries_on_connection_error(monkeypatch):
    project = Mock()
    monkeypatch.setattr(scheduler, "_job_settings", Mock(return_value={}))
    monkeypatch.setattr(scheduler.time, "sleep", Mock())

    run = project.spiders.get.return_value.jobs.run
    run.side_effect = [requests.exceptions.ConnectionError("boom"), None]

    scheduler._schedule_job(
        start="2026-08-01", full=False, spider_name="test_spider", project=project
    )

    assert run.call_count == 2


def test_schedule_job_raises_after_exhausting_retries(monkeypatch):
    project = Mock()
    monkeypatch.setattr(scheduler, "_job_settings", Mock(return_value={}))
    monkeypatch.setattr(scheduler.time, "sleep", Mock())

    run = project.spiders.get.return_value.jobs.run
    run.side_effect = requests.exceptions.ConnectionError("boom")

    with pytest.raises(requests.exceptions.ConnectionError):
        scheduler._schedule_job(
            start="2026-08-01", full=False, spider_name="test_spider", project=project
        )

    assert run.call_count == scheduler.SCHEDULE_JOB_RETRY_ATTEMPTS


def test_schedule_enabled_spiders_continues_after_one_spider_fails(monkeypatch):
    project = Mock()
    monkeypatch.setattr(scheduler, "_get_project", Mock(return_value=project))
    monkeypatch.setattr(
        scheduler,
        "_get_enabled_spiders",
        Mock(return_value=["first_spider", "second_spider", "third_spider"]),
    )
    schedule_job = Mock(
        side_effect=[
            None,
            requests.exceptions.ConnectionError("boom"),
            None,
        ]
    )
    monkeypatch.setattr(scheduler, "_schedule_job", schedule_job)

    with pytest.raises(click.ClickException, match="second_spider"):
        scheduler.schedule_enabled_spiders.callback()

    # os três spiders foram tentados, mesmo o segundo tendo falhado
    assert schedule_job.call_count == 3
    scheduled_names = [
        call.kwargs["spider_name"] for call in schedule_job.call_args_list
    ]
    assert scheduled_names == ["first_spider", "second_spider", "third_spider"]
