from flask import Flask, render_template
from tic_tac_toe import TicTacToe
from rat import solve_rat_maze
from water import run_water_jug_solver_gui
from puzzle import PuzzleGUI
import tkinter as tk
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/playtic')
def play_tictactoe():
    game = TicTacToe()
    game.mainloop()  # Ensure that TicTacToe has a mainloop() function to run the game
    return 'TicTacToe game over'

@app.route('/playrat')
def play_rat_in_maze():
    
    solve_rat_maze()  # Ensure that Rat in a Maze has a mainloop() function to run the game
    return 'Rat in a Maze game over'
@app.route('/playjug')
def play_water_jug():
   run_water_jug_solver_gui()
   return 'Water jug game over' 

@app.route('/playpuzzle')
def play_eight_puzzle():
    root = tk.Tk()  # Instantiate a Tkinter root window
    PuzzleGUI(root)  # Pass the root window as the master argument
    root.mainloop()  # Run the Tkinter event loop
    return 'Eight puzzle game over'



if __name__ == '__main__':
    app.run(debug=True)


