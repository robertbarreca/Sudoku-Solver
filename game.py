from tkinter import *
import copy
import time
import ending_page
import solver


# Function to create the game board
def run_game(difficulty):
    """
    run_game sets up the sudoku board so the user can play it
    """
    start_time = time.time() + 1
    error_time = 0
    error_ct = 0
    timer_callback = None
    entries = [[None for _ in range(9)] for _ in range(9)]

    def update_board(i, j, num):
        entry = entries[i][j]
        if num > 0:
            entry.delete(0, "end")
            entry.insert(0, num)
        else:
            entry.delete(0, "end")
        entry.update()  # Update the entry widget to reflect the changes immediately

    def end_game(elapsed_time, err_ct):
        """
        end_game is called when the user completes the sudoku board, it stops the time, and loads the ending page
        """
        nonlocal timer_callback
        if timer_callback:
            game.after_cancel(timer_callback)  # Cancel any pending timer updates
        # start the end page
        ending_page.main(elapsed_time, err_ct)
        game.quit()  # End the Tkinter mainloop properly

    def validate_input(char, val):
        """
        validate_input checks whether the user can place a character in its selected entry
        :param char: the character to be validated
        :param val: the current value inside the entry
        :return: true if the char is a number 1-9 and the value inside the entry is one character
        """
        return char.isdigit() and 1 <= int(char) <= 9 and len(val) <= 1

    def on_enter(event):
        """
        on_enter handles the Enter key press event. If the entered number can lead to a solution, mark the entry as read-only. Otherwise, indicate an incorrect attempt and adjust the timer
        """
        nonlocal error_time, error_ct
        entry = event.widget
        row, col = entry.row, entry.col

        # cache board if it needs to be reverted
        starter_board = copy.deepcopy(solver.board)

        num = int(entry.get())
        solver.board[row][col] = num
        starter_board[row][col] = num
        solvable = solver.validate() and solver.solve()
        # if it can lead to a solution set as read-only and tell user it's right
        if solvable:
            entry.config(bg="#43A047", fg="white")
            game.after(
                500,
                lambda e=entry: [
                    e.config(bg="white", fg="black"),
                    e.config(state="readonly"),
                ],
            )
            solver.board = starter_board
            # board is complete go to next page
            if all(0 not in row for row in solver.board):
                end_game(int(time.time() - start_time + error_time), error_ct)
            return
        else:
            entry.config(bg="#ED4337", fg="white")
            game.after(500, lambda: entry.config(bg="white", fg="black"))
            timer_value.config(fg="#ED4337")
            err_value.config(fg="#ED4337")
            game.after(500, lambda: timer_value.config(fg="black"))
            game.after(500, lambda: err_value.config(fg="black"))
            solver.board = starter_board
            solver.board[row][col] = 0
            error_time += 15
            error_ct += 1
            err_value.config(text=str(error_ct))
            return

    def update_time():
        """
        update_time sets the label every 100 ms to convey how long it's been since the user started the game
        """
        nonlocal timer_callback
        if game.winfo_exists():  # Ensure the game window still exists before updating
            elapsed_time = int(time.time() - start_time + error_time)
            mins = elapsed_time // 60
            secs = elapsed_time % 60
            timer_value.config(text=f"{mins:02d}:{secs:02d}")
            timer_text.config(text=f"Elapsed time: ")
            # Schedule the next update and store the callback
            timer_callback = game.after(100, update_time)

    def solve_board():
        """
        solve_board visualizes the backtracking algorithm solving the given board
        """
        nonlocal error_time, error_ct
        solver.solve_iteratively(update_board)
        for i in range(9):
            for j in range(9):
                entries[i][j].config(state="readonly")
        end_game(int(time.time() - start_time + error_time), error_ct)

    global game
    game = Tk()
    game.title("Sudoku Game")
    game.geometry("630x540")

    # Create a Frame to hold the Sudoku board
    board_frame = Frame(game, borderwidth=2, relief="solid")
    board_frame.pack(side="top", padx=10, pady=15)

    solver.fetch(difficulty)

    # Create a 9x9 grid of Entry widgets inside 3x3 boxes
    for i in range(3):
        for j in range(3):
            box_frame = Frame(board_frame, borderwidth=1, relief="solid")
            box_frame.grid(row=i, column=j, padx=1, pady=1)

            for m in range(3):
                for n in range(3):
                    # do conversion for rows and cols
                    row = i * 3 + m
                    col = j * 3 + n
                    # get val from starter board
                    val = solver.board[row][col]
                    entry = Entry(
                        box_frame,
                        width=2,
                        font=("Arial", 30),
                        justify="center",
                        validate="key",
                        highlightcolor="gray",
                    )
                    entry.grid(row=m, column=n, padx=1, pady=1)
                    entries[row][col] = entry
                    if val != 0:
                        entry.insert(0, val)
                        entry.config(state="readonly")
                    else:
                        entry.config(
                            validatecommand=(entry.register(validate_input), "%S", "%P")
                        )
                        entry.bind("<Return>", on_enter)
                        entry.row, entry.col = row, col

    # Create a Frame to hold the timer and the label, and solve button
    bottom_frame = Frame(game)
    bottom_frame.pack(side="bottom", fill="x")

    # Sub-frame to group the timer text and value
    timer_frame = Frame(bottom_frame)
    timer_frame.pack(side="right", pady=15, padx=15)

    # "Elapsed Time:" text label
    timer_text = Label(timer_frame, text="Elapsed Time:", font=("Arial", 18))
    timer_text.pack(side="left")

    # "00:00" value label
    timer_value = Label(timer_frame, text="00:00", font=("Arial", 18))
    timer_value.pack(side="left")

    # Mistake display
    err_text = Label(bottom_frame, text="Mistake Count:", font=("Arial", 18))
    err_text.pack(side="left", padx=(15, 0), pady=15)
    err_value = Label(bottom_frame, text="0", font=("Arial", 18))
    err_value.pack(side="left", padx=(0, 15), pady=15)

    # solve board button
    solve_button = Button(
        bottom_frame, text="Solve Board", command=solve_board, font=("Arial", 18)
    )
    solve_button.pack(side="bottom", pady=15)

    # Start the timer
    start_time = time.time()
    update_time()

    game.mainloop()
