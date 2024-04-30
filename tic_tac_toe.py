import tkinter as tk
from tkinter import messagebox
from collections import deque

class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self.geometry("300x400")
        self.configure(bg="#f0f0f0")

        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.player = 'X'
        self.moves = [(i, j) for i in range(3) for j in range(3)]
        self.buttons = []        
        self.winning_moves = {'X': 0, 'O': 0}  # Initialize winning moves count

        self.create_board()
        self.create_buttons()

    def create_board(self):
        board_frame = tk.Frame(self, bg="#f0f0f0")
        board_frame.pack(pady=10)

        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(board_frame, text='', width=6, height=3, font=("Arial", 12),
                                   bg="#ffffff", fg="#333333", bd=0, command=lambda i=i, j=j: self.click(i, j))
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)

    def create_buttons(self):
        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=10)

        reset_button = tk.Button(button_frame, text='Reset', font=("Arial", 12), bg="#5cb85c", fg="#ffffff",
                                 bd=0, padx=10, pady=5, command=self.reset)
        reset_button.grid(row=0, column=0, padx=10)

        player_button = tk.Button(button_frame, text='Choose Player (X/O)', font=("Arial", 12),
                                  bg="#5bc0de", fg="#ffffff", bd=0, padx=10, pady=5, command=self.choose_player)
        player_button.grid(row=0, column=1, padx=10)

    def click(self, i, j):
        if self.board[i][j] == '' and not self.check_winner():
            self.board[i][j] = self.player
            self.buttons[i][j].config(text=self.player)
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.player} wins!")
                self.winning_moves[self.player] += 1  # Update winning moves count
                self.display_winning_moves()
                self.reset()
            elif all(self.board[i][j] != '' for i in range(3) for j in range(3)):
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset()
            else:
                self.player = 'O' if self.player == 'X' else 'X'
                self.computer_move()

    def reset(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.player = 'X'
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='')

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True
        return False

    def computer_move(self):
        q = deque([(self.board, self.player)])
        while q:
            board, player = q.popleft()
            if self.check_winner():
                return
            for i, j in self.moves:
                if board[i][j] == '':
                    new_board = [row[:] for row in board]
                    new_board[i][j] = 'X' if player == 'O' else 'O'
                    if not self.check_winner():
                        q.append((new_board, 'X' if player == 'O' else 'O'))
                        if len(q) > 10**6:
                            return
                    else:
                        self.board[i][j] = 'O' if player == 'X' else 'X'
                        self.buttons[i][j].config(text=self.board[i][j])
                        if self.check_winner():
                            messagebox.showinfo("Game Over", f"Player {self.player} wins!")
                            self.winning_moves[self.player] += 1  # Update winning moves count
                            self.display_winning_moves()
                            self.reset()
                        elif all(self.board[i][j] != '' for i in range(3) for j in range(3)):
                            messagebox.showinfo("Game Over", "It's a draw!")
                            self.reset()
                        return

    def choose_player(self):
        self.reset()
        choice = messagebox.askquestion("Choose Player", "Do you want to play as X?")
        if choice == 'yes':
            self.player = 'X'
        else:
            self.player = 'O'
            self.computer_move()

    def display_winning_moves(self):
        messagebox.showinfo("Winning Moves", f"Player X wins: {self.winning_moves['X']}\nPlayer O wins: {self.winning_moves['O']}")

if __name__ == "__main__":
    game = TicTacToe()
    game.mainloop()