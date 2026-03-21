"""Integration tests for Stats endpoints."""

import uuid
from datetime import datetime, timezone

STATS_BREWS = "/api/v1/stats/brews"
STATS_BEANS = "/api/v1/stats/beans"
STATS_TASTE = "/api/v1/stats/taste"
STATS_EQUIPMENT = "/api/v1/stats/equipment"
STATS_CUPPINGS = "/api/v1/stats/cuppings"

# Reusable endpoint constants for creating seed data
PEOPLE = "/api/v1/people"
BEANS = "/api/v1/beans"
BREW_METHODS = "/api/v1/brew-methods"
BREW_SETUPS = "/api/v1/brew-setups"
BREWS = "/api/v1/brews"
GRINDERS = "/api/v1/grinders"
BREWERS = "/api/v1/brewers"
PAPERS = "/api/v1/papers"
WATERS = "/api/v1/waters"
FLAVOR_TAGS = "/api/v1/flavor-tags"
ROASTERS = "/api/v1/roasters"
ORIGINS = "/api/v1/origins"
CUPPINGS = "/api/v1/cuppings"
RATINGS = "/api/v1/beans"  # ratings are nested: /beans/{id}/ratings
BEAN_RATINGS = "/api/v1/bean-ratings"  # taste sub-resource: /bean-ratings/{id}/taste


# ======================================================================
# Helpers
# ======================================================================


def _unique(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _create_person(client, name: str | None = None) -> str:
    name = name or _unique("person")
    resp = client.post(PEOPLE, json={"name": name})
    assert resp.status_code == 201
    return resp.json()["id"]


def _create_bean(client, name: str | None = None, **kwargs) -> str:
    name = name or _unique("bean")
    payload = {"name": name, **kwargs}
    resp = client.post(BEANS, json=payload)
    assert resp.status_code == 201
    return resp.json()["id"]


def _create_bag(client, bean_id: str, **kwargs) -> str:
    payload = {"weight": 250.0, **kwargs}
    resp = client.post(f"{BEANS}/{bean_id}/bags", json=payload)
    assert resp.status_code == 201
    return resp.json()["id"]


def _create_brew_method(client, name: str | None = None) -> str:
    name = name or _unique("method")
    resp = client.post(BREW_METHODS, json={"name": name})
    assert resp.status_code == 201
    return resp.json()["id"]


def _create_brew_setup(
    client,
    brew_method_id: str,
    grinder_id: str | None = None,
    brewer_id: str | None = None,
    **kwargs,
) -> str:
    payload = {"brew_method_id": brew_method_id, **kwargs}
    if grinder_id:
        payload["grinder_id"] = grinder_id
    if brewer_id:
        payload["brewer_id"] = brewer_id
    resp = client.post(BREW_SETUPS, json=payload)
    assert resp.status_code == 201
    return resp.json()["id"]


def _create_brew(
    client,
    bag_id: str,
    brew_setup_id: str,
    person_id: str,
    dose: float = 18.0,
    **kwargs,
) -> str:
    payload = {
        "bag_id": bag_id,
        "brew_setup_id": brew_setup_id,
        "person_id": person_id,
        "dose": dose,
        "brewed_at": kwargs.pop("brewed_at", _now_iso()),
        **kwargs,
    }
    resp = client.post(BREWS, json=payload)
    assert resp.status_code == 201
    return resp.json()["id"]


def _create_grinder(client, name: str | None = None) -> str:
    name = name or _unique("grinder")
    resp = client.post(GRINDERS, json={"name": name})
    assert resp.status_code == 201
    return resp.json()["id"]


def _create_brewer(client, name: str | None = None) -> str:
    name = name or _unique("brewer")
    resp = client.post(BREWERS, json={"name": name})
    assert resp.status_code == 201
    return resp.json()["id"]


def _create_flavor_tag(client, name: str | None = None) -> str:
    name = name or _unique("tag")
    resp = client.post(FLAVOR_TAGS, json={"name": name})
    assert resp.status_code == 201
    return resp.json()["id"]


def _create_roaster(client, name: str | None = None) -> str:
    name = name or _unique("roaster")
    resp = client.post(ROASTERS, json={"name": name})
    assert resp.status_code == 201
    return resp.json()["id"]


def _create_origin(client, name: str | None = None, **kwargs) -> str:
    name = name or _unique("origin")
    resp = client.post(ORIGINS, json={"name": name, **kwargs})
    assert resp.status_code == 201
    return resp.json()["id"]


# ======================================================================
# GET /stats/brews
# ======================================================================


class TestBrewStats:
    """Tests for GET /api/v1/stats/brews."""

    def test_empty_state(self, client):
        """No brews → zero counts, None averages."""
        resp = client.get(STATS_BREWS)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0
        assert data["this_week"] == 0
        assert data["this_month"] == 0
        assert data["total_failed"] == 0
        assert data["fail_rate"] is None
        assert data["avg_dose_g"] is None
        assert data["avg_yield_g"] is None
        assert data["avg_brew_time_s"] is None
        assert data["last_brewed_at"] is None
        assert data["by_method"] == []

    def test_with_brews(self, client):
        """Seed brews and verify counts and averages."""
        person_id = _create_person(client)
        bean_id = _create_bean(client)
        bag_id = _create_bag(client, bean_id)
        method_id = _create_brew_method(client)
        setup_id = _create_brew_setup(client, method_id)

        # Create 2 brews: one successful, one failed
        _create_brew(
            client, bag_id, setup_id, person_id,
            dose=18.0, yield_amount=36.0, total_time=30.0,
        )
        _create_brew(
            client, bag_id, setup_id, person_id,
            dose=20.0, yield_amount=40.0, total_time=25.0, is_failed=True,
        )

        resp = client.get(STATS_BREWS, params={"person_id": person_id})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        assert data["this_week"] == 2
        assert data["this_month"] == 2
        assert data["total_failed"] == 1
        assert data["fail_rate"] == 0.5
        assert data["avg_dose_g"] == 19.0
        assert data["avg_yield_g"] == 38.0
        assert data["avg_brew_time_s"] == 27.5
        assert data["last_brewed_at"] is not None
        assert len(data["by_method"]) == 1
        assert data["by_method"][0]["count"] == 2

    def test_person_filter(self, client):
        """Stats only count brews for the specified person."""
        person_a = _create_person(client)
        person_b = _create_person(client)
        bean_id = _create_bean(client)
        bag_id = _create_bag(client, bean_id)
        method_id = _create_brew_method(client)
        setup_id = _create_brew_setup(client, method_id)

        _create_brew(client, bag_id, setup_id, person_a, dose=18.0)
        _create_brew(client, bag_id, setup_id, person_b, dose=20.0)

        resp = client.get(STATS_BREWS, params={"person_id": person_a})
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

    def test_nonexistent_person_404(self, client):
        """Explicit unknown person_id returns 404."""
        fake_id = str(uuid.uuid4())
        resp = client.get(STATS_BREWS, params={"person_id": fake_id})
        assert resp.status_code == 404

    def test_retired_person_404(self, client):
        """Explicit retired person_id returns 404."""
        person_id = _create_person(client)
        resp = client.delete(f"{PEOPLE}/{person_id}")
        assert resp.status_code == 200

        resp = client.get(STATS_BREWS, params={"person_id": person_id})
        assert resp.status_code == 404
