"""Similarity matching service for transfer learning.

Finds beans similar to a target bean by process + variety, used to seed
BayBE campaigns via transfer learning (TaskParameter) when a new bean is
added that shares characteristics with already-dialed-in beans.

Similarity is strict: BOTH process AND variety must be non-null and match.
Missing metadata = no match.
"""

from dataclasses import dataclass

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.bean import Bean
from app.models.brew_setup import BrewSetup
from app.models.measurement import Measurement


@dataclass
class SimilarBean:
    """A bean similar to the target, with enough measurement data to contribute priors."""

    bean_id: str
    bean_name: str
    process: str | None
    variety: str | None
    measurement_count: int


class SimilarityService:
    """Find similar beans for transfer learning seeding."""

    def count_method_measurements(self, bean_id: str, method: str, db: Session) -> int:
        """Count measurements for a given bean + brew method combination.

        Args:
            bean_id: The bean UUID.
            method: Brew method name (e.g. "espresso", "pour-over").
            db: SQLAlchemy session.

        Returns:
            Number of measurements for this bean+method.
        """
        # Espresso measurements: NULL brew_setup_id (legacy) OR brew_setup.brew_method.name == "espresso"
        # Pour-over / other: brew_setup.brew_method.name == method
        if method == "espresso":
            # Count legacy (no setup) + setup-linked espresso measurements
            legacy_count = (
                db.query(func.count(Measurement.id))
                .filter(
                    Measurement.bean_id == bean_id,
                    Measurement.brew_setup_id.is_(None),
                )
                .scalar()
                or 0
            )
            setup_count = (
                db.query(func.count(Measurement.id))
                .join(Measurement.brew_setup)
                .join(BrewSetup.brew_method)
                .filter(
                    Measurement.bean_id == bean_id,
                    Measurement.brew_setup_id.isnot(None),
                )
                .filter(BrewSetup.brew_method.has(name="espresso"))
                .scalar()
                or 0
            )
            return legacy_count + setup_count
        else:
            return (
                db.query(func.count(Measurement.id))
                .join(Measurement.brew_setup)
                .join(BrewSetup.brew_method)
                .filter(
                    Measurement.bean_id == bean_id,
                )
                .filter(BrewSetup.brew_method.has(name=method))
                .scalar()
                or 0
            )

    def find_similar_beans(
        self,
        target_bean: Bean,
        method: str,
        db: Session,
        min_measurements: int = 3,
    ) -> list[SimilarBean]:
        """Find beans with matching process + variety that have enough measurement data.

        Returns empty list if:
        - target_bean has no process or no variety
        - No other beans share both process AND variety
        - Matching beans have fewer than min_measurements for the given method

        Args:
            target_bean: The bean to find similar beans for.
            method: Brew method name — only counts measurements for this method.
            db: SQLAlchemy session.
            min_measurements: Minimum measurements required to be included (default 3).

        Returns:
            List of SimilarBean, ordered by measurement_count DESC.
        """
        # Can't match on missing metadata
        if not target_bean.process or not target_bean.variety:
            return []

        # Find candidate beans with matching process + variety (excluding target)
        candidates = (
            db.query(Bean)
            .filter(
                Bean.id != target_bean.id,
                Bean.process == target_bean.process,
                Bean.variety == target_bean.variety,
            )
            .all()
        )

        if not candidates:
            return []

        # Filter by measurement count and build result list
        results: list[SimilarBean] = []
        for bean in candidates:
            count = self.count_method_measurements(bean.id, method, db)
            if count >= min_measurements:
                results.append(
                    SimilarBean(
                        bean_id=bean.id,
                        bean_name=bean.name,
                        process=bean.process,
                        variety=bean.variety,
                        measurement_count=count,
                    )
                )

        # Order by measurement count DESC (most data first)
        results.sort(key=lambda b: b.measurement_count, reverse=True)
        return results
