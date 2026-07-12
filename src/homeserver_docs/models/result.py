from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class Result(Generic[T]):
    """Generic result returned by collectors."""

    data: T
    source: str