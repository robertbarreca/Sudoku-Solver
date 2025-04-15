from tkinter import *
import landing_page as landing_page
import game as game


def main(elapsed_time, err_ct):
    """
    main sets up the ending_page
    """
    # format how long it took user to play game
    mins = elapsed_time // 60
    secs = elapsed_time % 60

    minute_str = "minutes" if mins != 1 else "minute"
    sec_str = "seconds" if mins != 1 else "second"
    err_str = "mistakes" if err_ct != 1 else "mistake"
    result_str = f"You completed the board in {mins} {minute_str} and {secs} {sec_str} and made {err_ct} {err_str}"

    ending_page = Tk()
    ending_page.title("Congratulations!")
    ending_page.geometry("550x300")

    # Add labels
    congrats_label = Label(
        ending_page,
        text="Congratulations!",
        font=("Arial", 16),
    )
    results_label = Label(
        ending_page,
        text=result_str,
        font=("Arial", 14),
    )
    question_label = Label(
        ending_page,
        text=f"Would you like to play again?",
        font=("Arial", 14),
    )
    congrats_label.pack(pady=20)
    results_label.pack(pady=20)
    question_label.pack(pady=20)

    def play_again():
        """
        play_again closes both the ending page and the game page, while opening a new landing page, so that the user can play again
        """
        ending_page.destroy()
        game.game.destroy()
        landing_page.main()

    def quit_session():
        """
        quit session closes both the ending page and the game page
        """
        ending_page.destroy()
        game.game.destroy()

    # add buttons
    buttons_frame = Frame(ending_page)
    buttons_frame.pack()

    no_button = Button(
        buttons_frame,
        text="No",
        font=("Arial", 12),
        command=quit_session,
        width=10,
        height=5,
    )
    yes_button = Button(
        buttons_frame,
        text="Yes",
        font=("Arial", 12),
        command=play_again,
        width=10,
        height=5,
    )

    no_button.pack(side="left", pady=10, padx=20)
    yes_button.pack(side="left", pady=10, padx=20)

    ending_page.mainloop()


if __name__ == "__main__":
    main(61, 3)
