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
