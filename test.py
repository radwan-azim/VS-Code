"""Generate a Sierpinski triangle fractal and export it as an SVG file.

This module provides a command line interface that can be used to create a
Sierpinski triangle of an arbitrary recursion depth. The output is saved as an
SVG file so that it can be viewed or post-processed without relying on any
external libraries beyond the Python standard library.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Iterable, Sequence, Tuple

Point = Tuple[float, float]
Triangle = Tuple[Point, Point, Point]


def midpoint(a: Point, b: Point) -> Point:
    """Return the midpoint between two 2D points."""

    return (a[0] / 2 + b[0] / 2, a[1] / 2 + b[1] / 2)


def sierpinski_triangles(order: int, triangle: Triangle) -> Iterable[Triangle]:
    """Recursively yield the solid triangles that compose the fractal.

    Args:
        order: Depth of the recursion. ``0`` corresponds to the base triangle.
        triangle: The starting triangle represented as a tuple of points.
    """

    if order < 0:
        raise ValueError("order must be a non-negative integer")

    if order == 0:
        yield triangle
        return

    a, b, c = triangle
    ab = midpoint(a, b)
    bc = midpoint(b, c)
    ca = midpoint(c, a)

    yield from sierpinski_triangles(order - 1, (a, ab, ca))
    yield from sierpinski_triangles(order - 1, (ab, b, bc))
    yield from sierpinski_triangles(order - 1, (ca, bc, c))


def create_equilateral_triangle(side_length: float) -> Triangle:
    """Return an equilateral triangle pointing upwards."""

    height = math.sqrt(3) / 2 * side_length
    return ((0.0, height), (side_length / 2, 0.0), (side_length, height))


def triangle_to_svg_path(triangle: Triangle) -> str:
    """Convert a triangle to an SVG path string."""

    (x1, y1), (x2, y2), (x3, y3) = triangle
    return f"M{x1:.6f},{y1:.6f} L{x2:.6f},{y2:.6f} L{x3:.6f},{y3:.6f} Z"


def triangles_to_svg(
    triangles: Sequence[Triangle],
    *,
    width: float,
    height: float,
    stroke: str = "none",
    fill: str = "#1f77b4",
    background: str = "white",
) -> str:
    """Create an SVG document describing the provided triangles."""

    paths = [
        f'<path d="{triangle_to_svg_path(tri)}" fill="{fill}" stroke="{stroke}" />'
        for tri in triangles
    ]
    paths_str = "\n    ".join(paths)
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{width}\" height=\"{height}\" "
        f"viewBox=\"0 0 {width} {height}\">\n"
        f"  <rect width=\"100%\" height=\"100%\" fill=\"{background}\" />\n"
        f"  {paths_str}\n"
        "</svg>\n"
    )


def write_svg(content: str, path: Path) -> None:
    """Write the SVG content to the provided path."""

    path.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a Sierpinski triangle SVG graphic.",
    )
    parser.add_argument(
        "--order",
        type=int,
        default=6,
        help="Recursion depth of the triangle (default: 6).",
    )
    parser.add_argument(
        "--side-length",
        type=float,
        default=800.0,
        help="Side length of the base equilateral triangle in SVG units (default: 800).",
    )
    parser.add_argument(
        "--fill",
        type=str,
        default="#1f77b4",
        help="Fill color for the triangles (default: #1f77b4).",
    )
    parser.add_argument(
        "--background",
        type=str,
        default="white",
        help="Background color for the SVG canvas (default: white).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("sierpinski_triangle.svg"),
        help="Output SVG file path (default: sierpinski_triangle.svg).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_triangle = create_equilateral_triangle(args.side_length)
    triangles = list(sierpinski_triangles(args.order, base_triangle))
    height = math.sqrt(3) / 2 * args.side_length
    svg = triangles_to_svg(
        triangles,
        width=args.side_length,
        height=height,
        fill=args.fill,
        background=args.background,
    )
    write_svg(svg, args.output)
    print(f"Sierpinski triangle saved to {args.output.resolve()}")


if __name__ == "__main__":
    main()
