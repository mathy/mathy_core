from typing import Any
import pytest

from mathy_core.expressions import BinaryExpression, MathExpression
from mathy_core.layout import TreeLayout, TreeMeasurement
from mathy_core.parser import (
    ExpressionParser,
    InvalidExpression,
    InvalidSyntax,
    TrailingTokens,
    UnexpectedBehavior,
)


def render_tree_to_text(expression: MathExpression) -> str:
    """Render a tree structure as ASCII text for terminal display.

    Args:
        input_text: The math expression text to parse and render

    Returns:
        A string containing the ASCII representation of the tree
    """
    layout = TreeLayout()
    measure: TreeMeasurement = layout.layout(
        expression, 6, 2
    )  # Adjusted units for better spacing

    # Calculate canvas dimensions
    padding = 4
    min_x = int(measure.minX - padding)
    max_x = int(measure.maxX + padding)
    min_y = int(measure.minY - padding)
    max_y = int(measure.maxY + padding)
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # Create empty canvas
    canvas = [[" " for _ in range(width)] for _ in range(height)]

    def draw_line(x1: int, y1: int, x2: int, y2: int) -> None:
        """Draw a line between two points using ASCII characters."""
        # Adjust coordinates to canvas space
        x1 = int(x1 - min_x)
        x2 = int(x2 - min_x)
        y1 = int(y1 - min_y)
        y2 = int(y2 - min_y)

        if x1 == x2:  # Vertical line
            for y in range(min(y1, y2), max(y1, y2) + 1):
                canvas[y][x1] = "│"
        elif y1 == y2:  # Horizontal line
            for x in range(min(x1, x2), max(x1, x2) + 1):
                canvas[y1][x] = "─"
        else:  # Diagonal lines
            # Calculate middle point for drawing corners
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2

            # Draw the diagonal connection
            if abs(x2 - x1) > 1:  # Only if there's enough space
                if y1 < y2:
                    canvas[mid_y][mid_x] = "╱" if x1 > x2 else "╲"
                else:
                    canvas[mid_y][mid_x] = "╲" if x1 > x2 else "╱"

    def node_visit(node: MathExpression, depth, data) -> None:
        """Visit each node and draw it on the canvas."""
        # Adjust coordinates to canvas space
        x = int(node.x - min_x)
        y = int(node.y - min_y)

        # Draw connection to parent
        if node.parent:
            parent_x = int(node.parent.x - min_x)
            parent_y = int(node.parent.y - min_y)
            draw_line(node.x, node.y, node.parent.x, node.parent.y)

        # Get node value
        value = str(node)
        if isinstance(node, BinaryExpression):
            value = node.name

        # Draw node
        node_width = len(value) + 2  # Add space for brackets
        start_x = x - node_width // 2

        # Draw node value
        if start_x >= 0 and start_x + node_width < width and y >= 0 and y < height:
            for i, char in enumerate(value):
                if start_x + i < width:
                    canvas[y][start_x + i] = char

    # Visit all nodes
    expression.visit_postorder(node_visit)

    # Trim empty rows and columns while preserving structure
    # Find bounds of actual content
    min_row = 0
    max_row = height - 1
    min_col = 0
    max_col = width - 1

    # Find first and last non-empty rows
    while min_row < height and all(c == " " for c in canvas[min_row]):
        min_row += 1
    while max_row > 0 and all(c == " " for c in canvas[max_row]):
        max_row -= 1

    # Find first and last non-empty columns
    while min_col < width and all(row[min_col] == " " for row in canvas):
        min_col += 1
    while max_col > 0 and all(row[max_col] == " " for row in canvas):
        max_col -= 1

    # Extract the trimmed canvas
    trimmed_canvas = [
        row[min_col : max_col + 1] for row in canvas[min_row : max_row + 1]
    ]

    # Convert canvas to string
    return "\n" + "\n".join("".join(row) for row in trimmed_canvas)


@pytest.mark.parametrize(
    "expectation",
    [
        {"input": "(3x^2) / (6x)", "output": "(3x^2) / 6x"},
        {"input": "4x * p^(1 + 3) * 12x^2", "output": "4x * p^(1 + 3) * 12x^2"},
        {
            "input": "(-2.257893300159429e+16h^2 * v) * j^4",
            "output": "(-2.257893300159429e + 16h^2 * v) * j^4",
        },
        {"input": "1f + 98i + 3f + 14t", "output": "1f + 98i + 3f + 14t"},
        {"input": "(5 * 3) * (32 / 7)", "output": "5 * 3 * 32 / 7"},
        {"input": "7 - 5 * 3 * (2^7)", "output": "7 - 5 * 3 * 2^7"},
        {"input": "(8x^2 * 9b) * 7", "output": "8x^2 * 9b * 7"},
        {"input": "(8 * 9b) * 7", "output": "8 * 9b * 7"},
        {"input": "7 - (5 * 3) * (32 / 7)", "output": "7 - 5 * 3 * 32 / 7"},
        {"input": "7 - (5 - 3) * (32 - 7)", "output": "7 - (5 - 3) * (32 - 7)"},
        {"input": "(7 - (5 * 3)) * (32 - 7)", "output": "(7 - 5 * 3) * (32 - 7)"},
    ],
)
def test_parser_to_string(expectation: dict[str, str]) -> None:
    parser = ExpressionParser()
    expression = parser.parse(expectation["input"])
    print(render_tree_to_text(expression))
    out_str = str(expression)
    print(render_tree_to_text(parser.parse(out_str)))
    assert out_str == expectation["output"]


def test_parser_factorials() -> None:
    """should parse factorials"""
    parser = ExpressionParser()
    expression = parser.parse("5!")
    # 5! = 5 * 4 * 3 * 2 * 1 = 120
    assert expression.evaluate() == 120


def test_parser_operator_precedence() -> None:
    expects: list[dict[str, float | int | str]] = [
        {"input": "9 / 8 * 9", "output": 10.125},
        {"input": "4 + 9 / 8 * 9", "output": 14.125},
    ]
    for expect in expects:
        parser = ExpressionParser()
        expression = parser.parse(str(expect["input"]))
        assert expression.evaluate() == expect["output"]


def test_parser_mult_exp_precedence() -> None:
    """should respect order of operations with factor parsing"""
    parser = ExpressionParser()
    expression = parser.parse("4x^2")
    val = expression.evaluate({"x": 2})
    # 4x^2 should evaluate to 16 with x=2
    assert val == 16

    expression = parser.parse("7 * 10 * 6x * 3x + 5x")
    assert expression is not None


@pytest.mark.parametrize(
    "expectation",
    [
        ["1=5+-", InvalidSyntax, "parse_unary not expected"],
        ["x+4^-", InvalidSyntax, "parse_unary not expected"],
        ["4^4/.", ValueError, "parse_unary coerce_to_number"],
        ["4*/", InvalidSyntax, "parse_mult not expected"],
        ["4+3+3     3", TrailingTokens, "_parse trailing tokens check"],
        ["4^+", InvalidSyntax, "parse_exponent check unary"],
        ["4+", UnexpectedBehavior, "parse_add not expected and not right"],
        ["", InvalidExpression, "_parse initial next check"],
        ["4=+", UnexpectedBehavior, "parse_equal not expected"],
        ["+!", InvalidSyntax, "parse_equal first check"],
        ["=+", InvalidSyntax, "parse_equal first check"],
    ],
)
def test_parser_exceptions(expectation: list[Any]) -> None:
    parser = ExpressionParser()
    in_str, out_err, meta = expectation
    with pytest.raises(out_err):
        parser.parse(in_str)
    assert meta != "", "add note about which parser fn throws for this case"
