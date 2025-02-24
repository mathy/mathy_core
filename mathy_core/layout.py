from typing import Any, Optional

from .expressions import BinaryExpression, MathExpression
from .tree import BinaryTreeNode


class TidierExtreme:
    left: Optional[BinaryTreeNode]
    right: Optional[BinaryTreeNode]
    thread: Optional[BinaryTreeNode]
    offset: float

    def __init__(self) -> None:
        self.left = None
        self.right = None
        self.thread = None
        self.offset = 0


class TreeMeasurement:
    """Summary of the rendered tree"""

    minX: float
    maxX: float
    minY: float
    maxY: float
    width: float
    height: float
    centerX: float
    centerY: float

    def __init__(self) -> None:
        self.minX = 10000
        self.maxX = 0
        self.minY = 10000
        self.maxY = 0
        self.width = 0
        self.height = 0
        self.centerX = 0
        self.centerY = 0


class TreeLayout:
    """Calculate a visual layout for input trees."""

    def layout(
        self,
        node: BinaryTreeNode,
        unit_x_multiplier: float = 1.0,
        unit_y_multiplier: float = 1.0,
    ) -> "TreeMeasurement":
        """Assign x/y values to all nodes in the tree, and return an object containing
        the measurements of the tree.

        Returns a TreeMeasurement object that describes the bounds of the tree"""
        self.measure(node)
        return self.transform(node, 0, unit_x_multiplier, unit_y_multiplier)

    def measure(
        self,
        node: Optional[BinaryTreeNode] = None,
        level: int = 0,
        extremes: Optional["TidierExtreme"] = None,
    ) -> "TreeLayout":
        if extremes is None:
            extremes = TidierExtreme()

        # left and right subtree extreme leaf nodes
        left_extremes = TidierExtreme()
        right_extremes = TidierExtreme()

        # separation at the root of the current subtree and current level.
        current_separation = 0.0
        root_separation = 0.0
        min_separation = 1.0

        # The offset from left/right children to the root of the current subtree.
        left_offset_sum = 0.0
        right_offset_sum = 0.0

        # Avoid selecting as extreme
        if not node:
            if extremes.left is not None:
                extremes.left.level = -1

            if extremes.right is not None:
                extremes.right.level = -1

            return self

        # Assign the `node.y`, note the left/right child nodes, and recurse
        node.y = level
        left = node.left
        right = node.right
        self.measure(left, level + 1, left_extremes)
        self.measure(right, level + 1, right_extremes)

        # A leaf is both the leftmost and rightmost node on the lowest level of the
        # subtree consisting of itself.
        if not node.right and not node.left:
            node.offset = 0
            extremes.right = extremes.left = node
            return self

        # if only a single child, assign the next available offset and return.
        if not node.right or not node.left:
            node.offset = min_separation
            extremes.right = extremes.left = node.left if node.left else node.right
            return self

        # Set the current separation to the minimum separation for the root of the
        # subtree.
        current_separation = min_separation
        left_offset_sum = right_offset_sum = 0

        # Traverse the subtrees until one of them is exhausted, pushing them apart
        # as needed.
        loops = 0
        while left and right:
            loops = loops + 1
            if loops > 100000:
                raise Exception("An impossibly large tree perhaps?")

            if current_separation < min_separation:
                root_separation += min_separation - current_separation
                current_separation = min_separation

            if left.right and left.offset:
                left_offset_sum += left.offset
                current_separation -= left.offset
                left = getattr(left, "thread", left.right)
            elif left.offset is not None:
                left_offset_sum -= left.offset
                current_separation += left.offset
                left = getattr(left, "thread", left.left)

            if right.left and right.offset:
                right_offset_sum -= right.offset
                current_separation -= right.offset
                right = getattr(right, "thread", right.left)
            elif right.offset is not None:
                right_offset_sum += right.offset
                current_separation += right.offset
                right = getattr(right, "thread", right.right)

        # Set the root offset, and include it in the accumulated offsets.
        node.offset = (root_separation + 1) / 2
        assert node.offset is not None
        left_offset_sum -= node.offset
        right_offset_sum += node.offset

        # Update right and left extremes
        right_left_level = getattr(right_extremes.left, "level", -1)
        left_left_level = getattr(left_extremes.left, "level", -1)
        if right_left_level > left_left_level or not node.left:
            extremes.left = right_extremes.left
            if extremes.left:
                assert extremes.left.offset is not None
                extremes.left.offset += node.offset

        else:
            extremes.left = left_extremes.left
            if extremes.left:
                assert extremes.left.offset is not None
                extremes.left.offset -= node.offset

        left_right_level = getattr(left_extremes.right, "level", -1)
        right_right_level = getattr(right_extremes.right, "level", -1)
        if left_right_level > right_right_level or not node.right:
            extremes.right = left_extremes.right
            if extremes.right:
                assert extremes.right.offset is not None
                extremes.right.offset -= node.offset

        else:
            extremes.right = right_extremes.right
            if extremes.right:
                assert extremes.right.offset is not None
                extremes.right.offset += node.offset

        # If the subtrees have uneven heights, check to see if they need to be
        # threaded.  If threading is required, it will affect only one node.
        if left and left != node.left and right_extremes and right_extremes.right:
            right_extremes.right.thread = left
            assert right_extremes.right.offset is not None
            right_extremes.right.offset = abs(
                right_extremes.right.offset + node.offset - left_offset_sum
            )
        elif right and right != node.right and left_extremes and left_extremes.left:
            left_extremes.left.thread = right
            assert left_extremes.left.offset is not None
            left_extremes.left.offset = abs(
                left_extremes.left.offset - node.offset - right_offset_sum
            )

        return self

    def transform(
        self,
        node: Optional[BinaryTreeNode] = None,
        x: float = 0,
        unit_x_multiplier: float = 1,
        unit_y_multiplier: float = 1,
        measure: Optional["TreeMeasurement"] = None,
    ) -> "TreeMeasurement":
        """Transform relative to absolute coordinates, and measure the bounds of
        the tree.

        Return a measurement of the tree in output units."""
        if measure is None:
            measure = TreeMeasurement()
        if not node:
            return measure
        node.x = x * unit_x_multiplier
        assert node.y is not None
        node.y *= unit_y_multiplier
        assert node.x is not None and node.offset is not None
        self.transform(
            node.left, x - node.offset, unit_x_multiplier, unit_y_multiplier, measure
        )
        self.transform(
            node.right, x + node.offset, unit_x_multiplier, unit_y_multiplier, measure
        )
        if measure.minY > node.y:
            measure.minY = node.y

        if measure.maxY < node.y:
            measure.maxY = node.y

        if measure.minX > node.x:
            measure.minX = node.x

        if measure.maxX < node.x:
            measure.maxX = node.x

        measure.width = abs(measure.minX - measure.maxX)
        measure.height = abs(measure.minY - measure.maxY)
        measure.centerX = measure.minX + measure.width / 2
        measure.centerY = measure.minY + measure.height / 2
        return measure


def render_tree_to_text(expression: MathExpression) -> str:
    """Render a tree structure as ASCII text for terminal display.

    Args:
        input_text: The math expression text to parse and render

    Returns:
        A string containing the ASCII representation of the tree
    """
    layout = TreeLayout()
    measure: TreeMeasurement = layout.layout(expression, 6, 2)  # type: ignore

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

    def node_visit(node: MathExpression, depth: int, data: Any) -> None:
        """Visit each node and draw it on the canvas."""
        # Adjust coordinates to canvas space
        x = int(node.x - min_x)  # type: ignore
        y = int(node.y - min_y)  # type: ignore

        # Draw connection to parent
        if node.parent:
            int(node.parent.x - min_x)  # type: ignore
            int(node.parent.y - min_y)  # type: ignore
            draw_line(node.x, node.y, node.parent.x, node.parent.y)  # type: ignore

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
        # fmt: off
        row[min_col:max_col + 1] for row in canvas[min_row:max_row + 1]
        # fmt: on
    ]

    # Convert canvas to string
    return "\n" + "\n".join("".join(row) for row in trimmed_canvas)


__all__ = ("TidierExtreme", "TreeMeasurement", "TreeLayout")
