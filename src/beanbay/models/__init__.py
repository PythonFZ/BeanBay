# Re-export all models so Alembic can discover them via SQLModel.metadata
from beanbay.models.person import Person  # noqa: F401
from beanbay.models.tag import (  # noqa: F401
    BeanVariety,
    BrewMethod,
    FlavorTag,
    Origin,
    ProcessMethod,
    Roaster,
    StopMode,
)
