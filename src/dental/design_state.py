"""Represent original and alternative smile-design states without changing motion."""
from dataclasses import dataclass


@dataclass(frozen=True)
class DentalDesignState:
    name: str
    mesh_path: str | None
    enabled: bool = True


ORIGINAL = DentalDesignState(name="original", mesh_path=None)
