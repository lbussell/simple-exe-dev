"""Services managed by systemd on this VM."""

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class Status(Enum):
    FAILED = 'failed'
    RUNNING = 'running'
    SCHEDULED = 'scheduled'
    NOT_RUNNING = 'not-running'

    @property
    def label(self) -> str:
        return self.value.replace('-', ' ').capitalize()


@dataclass(frozen=True)
class Schedule:
    next_run: datetime
    last_run: datetime | None


@dataclass(frozen=True)
class Service:
    name: str
    description: str
    status: Status
    schedule: Schedule | None


@dataclass(frozen=True)
class ServiceDetail(Service):
    since: datetime | None  # when it started running, or failed
    starts_at_boot: bool | None
    pid: int | None
    unit_file: str


def _status(active: str, sub: str, schedule: Schedule | None) -> Status:
    """Boil systemd's active and sub states down to what a maintainer cares about."""
    if active == 'failed' or sub == 'auto-restart':
        return Status.FAILED
    if sub == 'running':
        return Status.RUNNING
    if schedule:
        return Status.SCHEDULED
    return Status.NOT_RUNNING


def _systemctl(*args: str) -> str:
    return subprocess.run(
        ['systemctl', '--no-pager', *args],
        capture_output=True, text=True, check=True,
    ).stdout


def _from_usec(usec: int | None) -> datetime | None:
    return datetime.fromtimestamp(usec / 1_000_000, timezone.utc) if usec else None


def _schedules() -> dict[str, Schedule]:
    """Schedules of timer-activated services, by service name."""
    return {
        t['activates']: Schedule(_from_usec(t['next']), _from_usec(t['last']))
        for t in json.loads(_systemctl('list-timers', '--all', '--output=json'))
        if t['activates'] and t['next']
    }


def get_services() -> list[Service]:
    schedules = _schedules()
    services = []
    for u in json.loads(_systemctl('list-units', '--type=service', '--all', '--output=json')):
        schedule = schedules.get(u['unit'])
        services.append(Service(
            u['unit'], u['description'], _status(u['active'], u['sub'], schedule), schedule,
        ))
    return services


def get_service(name: str) -> ServiceDetail | None:
    """One service, or None if systemd doesn't know it."""
    keys = [
        'LoadState', 'ActiveState', 'SubState', 'Description', 'StateChangeTimestamp',
        'UnitFileState', 'MainPID', 'FragmentPath',
    ]
    output = _systemctl('show', '--timestamp=unix', '--property=' + ','.join(keys), '--', name)
    values = dict(line.split('=', 1) for line in output.splitlines())
    if values['LoadState'] == 'not-found':
        return None
    schedule = _schedules().get(name)
    status = _status(values['ActiveState'], values['SubState'], schedule)
    changed = values['StateChangeTimestamp'].removeprefix('@')
    return ServiceDetail(
        name=name,
        description=values['Description'],
        status=status,
        schedule=schedule,
        since=datetime.fromtimestamp(int(changed), timezone.utc)
        if changed and status in (Status.RUNNING, Status.FAILED) else None,
        # Only enabled/disabled units are started at boot by themselves; others are started by something else.
        starts_at_boot={'enabled': True, 'disabled': False}.get(values['UnitFileState']),
        pid=int(values['MainPID']) or None,
        unit_file=values['FragmentPath'],
    )
