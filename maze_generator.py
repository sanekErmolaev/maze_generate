import matplotlib.pyplot as plt
from dataclasses import dataclass, field
import random


@dataclass
class MazeCell:
    x: int
    y: int
    component: int
    is_open: bool = field(default=False)
    walls: list = field(default_factory=lambda: [True, True, True, True])  # walls: [top, right, bottom, left]


N = 30
LINE_WIDTH = 50


def find(cell, parent):
    if parent[cell] != cell:
        parent[cell] = find(parent[cell], parent)
    return parent[cell]


def union(cell1, cell2, parent, rank):
    root1 = find(cell1, parent)
    root2 = find(cell2, parent)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        elif rank[root1] < rank[root2]:
            parent[root1] = root2
        else:
            parent[root2] = root1
            rank[root1] += 1


def maze_generate(size):
    maze = [[MazeCell(x, y, x * size + y) for y in range(size)] for x in range(size)]
    parent = {(x, y): (x, y) for x in range(size) for y in range(size)}
    rank = {(x, y): 0 for x in range(size) for y in range(size)}

    while len(set(find((x, y), parent) for x in range(size) for y in range(size))) > 1:
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        direction = random.choice(['top', 'right', 'bottom', 'left'])

        if direction == 'top' and y > 0:
            if find((x, y), parent) != find((x, y - 1), parent):
                union((x, y), (x, y - 1), parent, rank)
                maze[x][y].walls[0] = False
                maze[x][y - 1].walls[2] = False
        elif direction == 'right' and x < size - 1:
            if find((x, y), parent) != find((x + 1, y), parent):
                union((x, y), (x + 1, y), parent, rank)
                maze[x][y].walls[1] = False
                maze[x + 1][y].walls[3] = False
        elif direction == 'bottom' and y < size - 1:
            if find((x, y), parent) != find((x, y + 1), parent):
                union((x, y), (x, y + 1), parent, rank)
                maze[x][y].walls[2] = False
                maze[x][y + 1].walls[0] = False
        elif direction == 'left' and x > 0:
            if find((x, y), parent) != find((x - 1, y), parent):
                union((x, y), (x - 1, y), parent, rank)
                maze[x][y].walls[3] = False
                maze[x - 1][y].walls[1] = False

    # Add entrance and exit
    maze[0][0].is_open = True
    maze[size - 1][size - 1].is_open = True

    return maze


maze = maze_generate(N)


def draw_maze(maze):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, N)
    ax.set_ylim(0, N)

    for x in range(N):
        for y in range(N):
            cell = maze[x][y]
            if cell.walls[0]:
                ax.plot([x, x + 1], [y, y], 'k-', lw=2)
            if cell.walls[1]:
                ax.plot([x + 1, x + 1], [y, y + 1], 'k-', lw=2)
            if cell.walls[2]:
                ax.plot([x, x + 1], [y + 1, y + 1], 'k-', lw=2)
            if cell.walls[3]:
                ax.plot([x, x], [y, y + 1], 'k-', lw=2)

    plt.show()


draw_maze(maze)