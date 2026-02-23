"""Campaign key helpers for multi-method brewing.

A campaign key uniquely identifies a BayBE optimization context:
    {bean_id}__{method}__{setup_id}

Examples:
    "abc123__espresso__setup456"
    "abc123__espresso__none"   # no setup selected
    "abc123__pour-over__setup789"
"""

SEPARATOR = "__"


def make_campaign_key(bean_id: str, method: str, setup_id: str | None) -> str:
    """Build a campaign key from its components.

    Args:
        bean_id: Bean UUID.
        method: Brew method name (e.g. "espresso", "pour-over").
        setup_id: Setup UUID, or None if no setup selected.

    Returns:
        Campaign key string like "abc123__espresso__setup456".
    """
    sid = setup_id or "none"
    return f"{bean_id}{SEPARATOR}{method}{SEPARATOR}{sid}"


def parse_campaign_key(key: str) -> tuple[str, str, str | None]:
    """Parse a campaign key into (bean_id, method, setup_id).

    Returns:
        (bean_id, method, setup_id) where setup_id is None if "none".
    """
    parts = key.split(SEPARATOR, 2)
    if len(parts) != 3:
        # Legacy bare bean_id key
        return key, "espresso", None
    bean_id, method, setup_id = parts
    return bean_id, method, (None if setup_id == "none" else setup_id)


def is_legacy_key(key: str) -> bool:
    """Return True if key is in the old bare-UUID format (no separators)."""
    return SEPARATOR not in key
