"""Read-only stats endpoints for dashboard widgets."""

import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter
from sqlalchemy import Integer
from sqlalchemy import func as sa_func
from sqlmodel import select

from beanbay.dependencies import OptionalPersonIdDep, SessionDep
from beanbay.models.bean import Bag, Bean, BeanOriginLink
from beanbay.models.brew import Brew, BrewSetup, BrewTaste, BrewTasteFlavorTagLink
from beanbay.models.cupping import Cupping, CuppingFlavorTagLink
from beanbay.models.equipment import Brewer, Grinder, Paper, Water
from beanbay.models.rating import BeanRating, BeanTaste, BeanTasteFlavorTagLink
from beanbay.models.tag import BrewMethod, FlavorTag, Roaster, Origin
from beanbay.schemas.stats import (
    BeanStatsRead,
    BeanTasteAxisAverages,
    BeanTasteStats,
    BrewStatsRead,
    BrewTasteAxisAverages,
    BrewTasteStats,
    CuppingStatsRead,
    EquipmentStatsRead,
    FlavorTagCount,
    MethodBrewCount,
    NamedUsageCount,
    OriginBeanCount,
    RoasterBeanCount,
    SetupUsage,
    TasteStatsRead,
)

router = APIRouter(tags=["Stats"])


def _r(val: float | None) -> float | None:
    """Round a float to 2 decimal places, or return None.

    Parameters
    ----------
    val : float | None
        Value to round.

    Returns
    -------
    float | None
        Rounded value, or ``None`` if input is ``None``.
    """
    return round(val, 2) if val is not None else None


def _week_start() -> datetime:
    """Return Monday 00:00 UTC of the current week.

    Returns
    -------
    datetime
        Monday midnight UTC of the current week.
    """
    now = datetime.now(timezone.utc)
    monday = now.replace(hour=0, minute=0, second=0, microsecond=0)
    monday -= timedelta(days=now.weekday())
    return monday


def _month_start() -> datetime:
    """Return 1st of current month 00:00 UTC.

    Returns
    -------
    datetime
        First day of the current month at midnight UTC.
    """
    now = datetime.now(timezone.utc)
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def _base_brew_filter(person_id: uuid.UUID | None):
    """Return base WHERE conditions for non-retired brews, optionally by person.

    Parameters
    ----------
    person_id : uuid.UUID | None
        If provided, filter brews to this person only.

    Returns
    -------
    list
        List of SQLAlchemy filter conditions.
    """
    conditions = [Brew.retired_at.is_(None)]  # type: ignore[union-attr]
    if person_id is not None:
        conditions.append(Brew.person_id == person_id)
    return conditions


@router.get("/stats/brews", response_model=BrewStatsRead)
def get_brew_stats(
    session: SessionDep,
    person_id: OptionalPersonIdDep,
) -> BrewStatsRead:
    """Aggregated brew statistics.

    Parameters
    ----------
    session : Session
        Database session.
    person_id : uuid.UUID | None
        Optional person filter resolved by dependency.

    Returns
    -------
    BrewStatsRead
        Aggregated brew statistics including counts, averages, and per-method breakdown.
    """
    conditions = _base_brew_filter(person_id)

    # Scalar aggregates
    row = session.exec(
        select(
            sa_func.count().label("total"),
            sa_func.sum(Brew.is_failed.cast(Integer)).label("total_failed"),  # type: ignore[union-attr]
            sa_func.avg(Brew.dose).label("avg_dose"),
            sa_func.avg(Brew.yield_amount).label("avg_yield"),
            sa_func.avg(Brew.total_time).label("avg_time"),
            sa_func.max(Brew.brewed_at).label("last_brewed"),
        ).where(*conditions)
    ).one()

    total = row.total or 0
    total_failed = int(row.total_failed or 0)

    # This week / this month
    week_start = _week_start()
    month_start = _month_start()

    this_week = session.exec(
        select(sa_func.count()).where(
            *conditions, Brew.brewed_at >= week_start
        )
    ).one()

    this_month = session.exec(
        select(sa_func.count()).where(
            *conditions, Brew.brewed_at >= month_start
        )
    ).one()

    # By method
    method_rows = session.exec(
        select(
            BrewMethod.id,
            BrewMethod.name,
            sa_func.count().label("cnt"),
        )
        .join(BrewSetup, BrewSetup.brew_method_id == BrewMethod.id)
        .join(Brew, Brew.brew_setup_id == BrewSetup.id)
        .where(*conditions)
        .group_by(BrewMethod.id, BrewMethod.name)
        .order_by(sa_func.count().desc())
    ).all()

    return BrewStatsRead(
        total=total,
        this_week=this_week,
        this_month=this_month,
        total_failed=total_failed,
        fail_rate=round(total_failed / total, 4) if total > 0 else None,
        avg_dose_g=round(row.avg_dose, 2) if row.avg_dose is not None else None,
        avg_yield_g=round(row.avg_yield, 2) if row.avg_yield is not None else None,
        avg_brew_time_s=round(row.avg_time, 2) if row.avg_time is not None else None,
        last_brewed_at=row.last_brewed,
        by_method=[
            MethodBrewCount(
                brew_method_id=r[0], brew_method_name=r[1], count=r[2]
            )
            for r in method_rows
        ],
    )
