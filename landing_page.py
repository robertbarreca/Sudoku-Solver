from tkinter import *
import game as game


def main():
    """
    main sets up the landing page gui
    """

    # Function to close the landing page and start the game
    def start_game(difficulty):
        """
        start_game starts the sudoku game based on the user's selected difficulty

        :param difficulty: what game mode the user wants to play (easy, medium, or hard)
        """
        landing_page.destroy()
        # create_game_board(difficulty)
        game.run_game(difficulty)

    # Landing page window
    landing_page = Tk()
    landing_page.title("Sudoku Game - Welcome")
    landing_page.geometry("500x300")

    # Add welcome text and buttons
    welcome_label = Label(
        landing_page,
        text="Welcome to Sudoku Game!",
        font=("Arial", 16),
    )
    welcome_label.pack(pady=20)

    choose_mode_label = Label(landing_page, text="Select your game mode to start:")
    choose_mode_label.pack()

    buttons_frame = Frame(landing_page)
    buttons_frame.pack()

    # Add buttons
    easy_button = Button(
        buttons_frame,
        text="Easy",
        command=lambda: start_game("easy"),
        width=10,
        height=5,
    )
    easy_button.pack(side="left", pady=60, padx=10, fill="both", expand=True)

    medium_button = Button(
        buttons_frame,
        text="Medium",
        command=lambda: start_game("medium"),
        width=10,
        height=5,
    )
    medium_button.pack(side="left", pady=60, padx=10, fill="both", expand=True)

    hard_button = Button(
        buttons_frame,
        text="Hard",
        command=lambda: start_game("hard"),
        width=10,
        height=5,
    )
    hard_button.pack(side="left", pady=60, padx=10, fill="both", expand=True)

    landing_page.mainloop()


if __name__ == "__main__":
    main()
