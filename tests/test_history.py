"""Tests for history router — shot history list with filters."""

import uuid
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.database import Base, SessionLocal, engine
from app.main import app
from app.models.bean import Bean
from app.models.measurement import Measurement


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def setup_db():
    """Create tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    """FastAPI test client."""
    return TestClient(app, follow_redirects=False)


@pytest.fixture()
def db():
    """Direct DB session for test setup."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def sample_bean(db):
    """Create a sample bean."""
    bean = Bean(name="Ethiopian Yirgacheffe", roaster="Onyx", origin="Ethiopia")
    db.add(bean)
    db.commit()
    db.refresh(bean)
    return bean


@pytest.fixture()
def second_bean(db):
    """Create a second sample bean."""
    bean = Bean(name="Colombian Huila", roaster="Counter Culture", origin="Colombia")
    db.add(bean)
    db.commit()
    db.refresh(bean)
    return bean


def _seed_shot(
    db,
    bean_id: str,
    taste: float = 8.0,
    is_failed: bool = False,
    notes: str | None = None,
    created_at: datetime | None = None,
) -> Measurement:
    """Seed a measurement directly into the DB."""
    m = Measurement(
        bean_id=bean_id,
        recommendation_id=str(uuid.uuid4()),
        grind_setting=20.0,
        temperature=93.0,
        preinfusion_pct=75.0,
        dose_in=19.0,
        target_yield=40.0,
        saturation="yes",
        taste=taste,
        is_failed=is_failed,
        notes=notes,
    )
    if created_at is not None:
        m.created_at = created_at
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_history_page_loads(client, sample_bean, db):
    """GET /history returns 200 and contains page title."""
    _seed_shot(db, sample_bean.id)
    response = client.get("/history")
    assert response.status_code == 200
    assert "Brew History" in response.text


def test_history_shows_shots_reverse_chronological(client, sample_bean, db):
    """Shots appear in newest-first order."""
    now = datetime.utcnow()
    shot_old = _seed_shot(db, sample_bean.id, taste=5.0, created_at=now - timedelta(hours=2))
    shot_mid = _seed_shot(db, sample_bean.id, taste=7.0, created_at=now - timedelta(hours=1))
    shot_new = _seed_shot(db, sample_bean.id, taste=9.0, created_at=now)

    response = client.get("/history")
    assert response.status_code == 200
    html = response.text

    # Newer shots should appear before older ones
    pos_new = html.find(f"shot-{shot_new.id}")
    pos_mid = html.find(f"shot-{shot_mid.id}")
    pos_old = html.find(f"shot-{shot_old.id}")

    assert pos_new < pos_mid < pos_old, "Shots should be in reverse-chronological order"


def test_history_filter_by_bean(client, sample_bean, second_bean, db):
    """GET /history/shots?bean_id=X returns only shots for that bean."""
    shot_a = _seed_shot(db, sample_bean.id, taste=8.0)
    shot_b = _seed_shot(db, second_bean.id, taste=7.0)

    response = client.get(f"/history/shots?bean_id={sample_bean.id}")
    assert response.status_code == 200
    html = response.text

    assert f"shot-{shot_a.id}" in html
    assert f"shot-{shot_b.id}" not in html


def test_history_filter_by_min_taste(client, sample_bean, db):
    """GET /history/shots?min_taste=7 returns only shots with taste >= 7."""
    shot_low = _seed_shot(db, sample_bean.id, taste=5.0)
    shot_mid = _seed_shot(db, sample_bean.id, taste=7.0)
    shot_high = _seed_shot(db, sample_bean.id, taste=9.0)

    response = client.get("/history/shots?min_taste=7")
    assert response.status_code == 200
    html = response.text

    assert f"shot-{shot_mid.id}" in html
    assert f"shot-{shot_high.id}" in html
    assert f"shot-{shot_low.id}" not in html


def test_history_combined_filters(client, sample_bean, second_bean, db):
    """Filter by bean AND min_taste together."""
    shot_match = _seed_shot(db, sample_bean.id, taste=8.0)
    shot_wrong_bean = _seed_shot(db, second_bean.id, taste=9.0)
    shot_low_taste = _seed_shot(db, sample_bean.id, taste=5.0)

    response = client.get(f"/history/shots?bean_id={sample_bean.id}&min_taste=7")
    assert response.status_code == 200
    html = response.text

    assert f"shot-{shot_match.id}" in html
    assert f"shot-{shot_wrong_bean.id}" not in html
    assert f"shot-{shot_low_taste.id}" not in html


def test_history_empty_state(client):
    """No shots → empty state message."""
    response = client.get("/history")
    assert response.status_code == 200
    assert "Start brewing" in response.text


def test_history_shows_failed_indicator(client, sample_bean, db):
    """Failed shot has 'Failed' badge in HTML."""
    _seed_shot(db, sample_bean.id, taste=1.0, is_failed=True)

    response = client.get("/history")
    assert response.status_code == 200
    assert "Failed" in response.text


def test_history_shows_notes_indicator(client, sample_bean, db):
    """Shot with notes shows the notes icon."""
    _seed_shot(db, sample_bean.id, notes="Very floral, slight brightness")

    response = client.get("/history")
    assert response.status_code == 200
    assert "Has notes" in response.text


def test_history_bean_preselect(client, sample_bean, db):
    """GET /history?bean_id=X renders that bean selected in the dropdown."""
    _seed_shot(db, sample_bean.id)

    response = client.get(f"/history?bean_id={sample_bean.id}")
    assert response.status_code == 200
    # The bean option should have 'selected' attribute
    assert "selected" in response.text
    assert sample_bean.name in response.text


def test_history_shots_partial_htmx(client, sample_bean, db):
    """GET /history/shots with HX-Request header returns partial only."""
    _seed_shot(db, sample_bean.id, taste=8.0)

    response = client.get(
        "/history/shots",
        headers={"HX-Request": "true"},
    )
    assert response.status_code == 200
    # Partial should NOT include the full base.html nav/head
    assert "<!DOCTYPE html>" not in response.text
    assert "BrewFlow" not in response.text
    # But should include the shot row
    assert "shot-row" in response.text
