"""Borders in Hearth for supported shapes."""
from dataclasses import dataclass
from typing import Optional

from forge.core.engine.color import Color


@dataclass(slots=True)
class Border:
    """
    Border for each supported shape in Hearth.
    """
    width: int
    color: Color
    radius: Optional[int] = None  # A border radius is only applicable to rectangles.
