import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import heapq

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, depth=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = 0
        self.heuristic = 0

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

    def get_blank_position(self):
        for i, row in enumerate(self.state):
            for j, cell in enumerate(row):
                if cell == 0:
                    return (i, j)

    def generate_children(self):
        blank_i, blank_j = self.get_blank_position()
        children = []
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < len(self.state) and 0 <= new_j < len(self.state[0]):
                new_state = [row[:] for row in self.state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                children.append(PuzzleNode(new_state, parent=self, move=(di, dj), depth=self.depth + 1))
        return children

    def manhattan_distance(self, goal_state):
        distance = 0
        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if self.state[i][j] != goal_state[i][j] and self.state[i][j] != 0:
                    x, y = divmod(goal_state[i][j], len(self.state[0]))
                    distance += abs(x - i) + abs(y - j)
        return distance

def solve_puzzle(initial_state, goal_state):
    open_set = []
    heapq.heappush(open_set, initial_state)
    closed_set = set()
    while open_set:
        current_node = heapq.heappop(open_set)
        closed_set.add(current_node)
        if current_node.state == goal_state:
            path = []
            while current_node.parent:
                path.append(current_node.move)
                current_node = current_node.parent
            return path[::-1]
        for child in current_node.generate_children():
            if child not in closed_set:
                child.cost = child.depth
                child.heuristic = child.manhattan_distance(goal_state)
                heapq.heappush(open_set, child)
    return None

class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("8-Puzzle Solver")

        self.initial_state = [[tk.StringVar() for _ in range(3)] for _ in range(3)]
        self.goal_state = [[tk.StringVar() for _ in range(3)] for _ in range(3)]

        self.create_input_widgets()
        self.create_solve_button()
        self.create_solution_display()

    def create_input_widgets(self):
        input_frame = ttk.Frame(self.master, padding=10)
        input_frame.grid(row=0, column=0, padx=10, pady=5)

        for i in range(3):
            for j in range(3):
                entry = ttk.Entry(input_frame, textvariable=self.initial_state[i][j], width=3, font=('Helvetica', 12))
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry = ttk.Entry(input_frame, textvariable=self.goal_state[i][j], width=3, font=('Helvetica', 12))
                entry.grid(row=i, column=j+4, padx=2, pady=2)

        ttk.Label(input_frame, text="Initial State", font=('Helvetica', 14)).grid(row=3, columnspan=3, pady=5)
        ttk.Label(input_frame, text="Goal State", font=('Helvetica', 14)).grid(row=3, column=4, columnspan=3, pady=5)

    def create_solve_button(self):
        solve_button = ttk.Button(self.master, text="Solve Puzzle", command=self.solve_puzzle)
        solve_button.grid(row=1, column=0, pady=10)

    def create_solution_display(self):
        solution_frame = ttk.Frame(self.master, padding=10)
        solution_frame.grid(row=2, column=0, padx=10, pady=5)

        self.solution_text = tk.Text(solution_frame, height=10, width=40, font=('Helvetica', 12))
        self.solution_text.grid(row=0, column=0, padx=5, pady=5)

    def solve_puzzle(self):
        initial_state = [[int(self.initial_state[i][j].get()) for j in range(3)] for i in range(3)]
        goal_state = [[int(self.goal_state[i][j].get()) for j in range(3)] for i in range(3)]

        solution_path = solve_puzzle(PuzzleNode(initial_state), goal_state)
        if solution_path:
            self.display_solution(solution_path)
        else:
            messagebox.showinfo("No Solution", "No solution found.")

    def display_solution(self, solution_path):
        self.solution_text.delete(1.0, tk.END)
        for step, move in enumerate(solution_path, 1):
            self.solution_text.insert(tk.END, f"Step {step}: Move {move}\n")
        self.solution_text.insert(tk.END, f"Number of moves: {len(solution_path)}")

    def visualize_puzzle_solution(self, solution_path):
        # Implement visualization here if needed
        pass

def run_puzzle_solver_gui():
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')
    app = PuzzleGUI(root)
    root.mainloop()

# Example usage:
# run_puzzle_solver_gui()

