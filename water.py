import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def jug_diagram_visualize(a, b, jug1, jug2):
    finalx = jug1 - a
    finaly = jug2 - b
    key = ['Jug 1', 'Jug 2']
    list1 = [a, b]
    list2 = [finalx, finaly]
    fig = Figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.bar(key, list1, color=['blue', 'green'])
    ax.bar(key, list2, bottom=list1, color=['white', 'white'], edgecolor='black')
    ax.set_xlabel("Jugs")
    ax.set_ylabel("Amount of Water (in L)")
    ax.set_title("Water Jug Problem")
    return fig

def water_jug_solver_visualize(jug1, jug2, goal):
    visited = set()
    stack = [(0, 0)]
    while stack:
        current_state = stack.pop()
        fig = jug_diagram_visualize(current_state[0], current_state[1], jug1, jug2)
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        if current_state[0] == goal or current_state[1] == goal:
            print("Goal achieved!")
            break
        visited.add(current_state)
        next_states = [
            (jug1, current_state[1]),  # Fill Jug1
            (current_state[0], jug2),  # Fill Jug2
            (0, current_state[1]),  # Empty Jug1
            (current_state[0], 0),  # Empty Jug2
            (max(0, current_state[0] - (jug2 - current_state[1])),
             min(jug2, current_state[1] + current_state[0])),  # Pour Jug1 to Jug2
            (min(jug1, current_state[0] + current_state[1]),
             max(0, current_state[1] - (jug1 - current_state[0])))  # Pour Jug2 to Jug1
        ]
        for state in next_states:
            if state not in visited:
                stack.append(state)

def run_water_jug_solver_gui():
    root = tk.Tk()
    root.title("Water Jug Problem Solver")

    jug1_label = tk.Label(root, text="Capacity of Jug 1:")
    jug1_label.pack()
    jug1_entry = tk.Entry(root)
    jug1_entry.pack()

    jug2_label = tk.Label(root, text="Capacity of Jug 2:")
    jug2_label.pack()
    jug2_entry = tk.Entry(root)
    jug2_entry.pack()

    goal_label = tk.Label(root, text="Desired amount to measure:")
    goal_label.pack()
    goal_entry = tk.Entry(root)
    goal_entry.pack()

    def solve():
        try:
            jug1_capacity = int(jug1_entry.get())
            jug2_capacity = int(jug2_entry.get())
            goal_amount = int(goal_entry.get())
            if jug1_capacity <= 0 or jug2_capacity <= 0 or goal_amount < 0:
                raise ValueError("Capacity and goal must be positive integers.")
            print("\nSteps:")
            water_jug_solver_visualize(jug1_capacity, jug2_capacity, goal_amount)
        except ValueError as e:
            tk.messagebox.showerror("Error", f"{e}. Please enter valid inputs.")

    solve_button = tk.Button(root, text="Solve", command=solve)
    solve_button.pack()

    root.mainloop()

# Example usage:
# run_water_jug_solver_gui()
