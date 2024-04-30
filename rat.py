import tkinter as tk
from tkinter import messagebox

def solve_rat_maze():
    # Using DFS approach for solving the problem
    def find_path(maze, start, goal):
        def dfs(current, path):
            if current == goal:
                return path + [current]

            x, y = current
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_x, next_y = x + dx, y + dy
                if (0 <= next_x < len(maze) and 0 <= next_y < len(maze[0]) and
                    maze[next_x][next_y] in (0, 3) and (next_x, next_y) not in path):
                    result = dfs((next_x, next_y), path + [current])
                    if result:
                        return result
            return None

        return dfs(start, [])

    def create_maze():
        maze = []
        for i in range(rows):
            row = []
            for j in range(columns):
                if (i, j) == start:
                    row.append(2)  # Mark start as 2
                elif (i, j) == goal:
                    row.append(3)  # Mark goal as 3
                elif (i, j) in walls:
                    row.append(1)  # 1 represents an obstacle
                else:
                    row.append(0)  # 0 represents an empty cell
            maze.append(row)
        return maze

    def solve_maze():
        maze = create_maze()
        path = find_path(maze, start, goal)
        if path:
            formatted_path = "->".join([f"({y},{x})" for x, y in path])  # Format path as (row, column)
            messagebox.showinfo("Path found", f"Path: {formatted_path}")
        else:
            messagebox.showinfo("No path found", "No path found")

    def toggle_wall(event):
        x, y = (event.x - cell_size) // cell_size, (event.y - cell_size) // cell_size
        if 0 <= x < columns and 0 <= y < rows:
            if (x, y) in {start, goal}:
                messagebox.showinfo("Warning", "Cannot change the start or goal point")
            elif (x, y) in walls:
                walls.remove((x, y))
                canvas.itemconfig(cells[y][x], fill="green")
            else:
                walls.add((x, y))
                canvas.itemconfig(cells[y][x], fill="red")

    # Create the main window
    root = tk.Tk()
    root.title("Rat in a Maze Solver")

    # Set maze parameters
    rows = 5
    columns = 5
    cell_size = 30

    # Create the canvas for the maze
    canvas = tk.Canvas(root, width=columns * cell_size + 20, height=rows * cell_size + 20)
    canvas.pack()

    # Create cells in the maze
    cells = []
    for i in range(rows):
        row = []
        for j in range(columns):
            cell = canvas.create_rectangle((j + 1) * cell_size, (i + 1) * cell_size, (j + 2) * cell_size, (i + 2) * cell_size, fill="green", outline="red")
            row.append(cell)
        cells.append(row)

    # Add row numbers on the top
    for i in range(rows):
        canvas.create_text((i + 1.5) * cell_size, 10, text=str(i), font=("Arial", 10))

    # Add column numbers on the side
    for j in range(columns):
        canvas.create_text(10, (j + 1.5) * cell_size, text=str(j), font=("Arial", 10))

    # Set starting and ending points
    start = (0, 0)
    goal = (rows - 1, columns - 1)

    # Add event binding to toggle walls
    walls = set()
    canvas.bind("<Button-1>", toggle_wall)

    # Create solve button
    solve_button = tk.Button(root, text="Solve Maze", command=solve_maze)
    solve_button.pack()

    # Run the application
    root.mainloop()

# When this file is executed, the main code will be run.
if __name__ == "__main__":
    solve_rat_maze()
