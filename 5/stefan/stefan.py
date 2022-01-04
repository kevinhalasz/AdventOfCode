from __future__ import annotations

from typing import IO, Optional

import attr


@attr.frozen
class Point:
    x: int = attr.ib(converter=int)
    y: int = attr.ib(converter=int)


@attr.frozen
class Line:
    start: Point
    end: Point

    @property
    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y

    @property
    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    @property
    def slope(self) -> float:
        if self.is_horizontal:
            return 0
        if self.is_vertical:
            return float("inf")

        return (self.end.y - self.start.y) / (self.end.x - self.start.x)

    @property
    def covered_points(self) -> Optional[list[Point]]:
        if self.is_horizontal:
            if self.start.x <= self.end.x:
                start = self.start.x
                end = self.end.x + 1
            else:
                start = self.end.x
                end = self.start.x + 1
            return [Point(x, self.start.y) for x in range(start, end)]

        elif self.is_vertical:
            if self.start.y <= self.end.y:
                start = self.start.y
                end = self.end.y + 1
            else:
                start = self.end.y
                end = self.start.y + 1
            return [Point(self.start.x, y) for y in range(start, end)]

        else:
            if self.start.x <= self.end.x:
                x_start = self.start.x
                y_start = self.start.y
                x_end = self.end.x + 1
            else:
                x_start = self.end.x
                y_start = self.end.y
                x_end = self.start.x + 1
            return [
                Point(x_start + i, y_start + i * self.slope)
                for i in range(x_end - x_start)
            ]

    @classmethod
    def from_input(cls, input_line: str) -> Line:
        start, end = input_line.split("->")
        return cls(Point(*start.strip().split(",")), Point(*end.strip().split(",")))
